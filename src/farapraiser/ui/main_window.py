"""Main window for FaraPraiser application."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QFileDialog, QMessageBox, QStatusBar, QToolBar, QLabel, QComboBox,
    QSpinBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from typing import List, Optional
import os

from farapraiser.parsers import get_parser, DocumentBlock
from farapraiser.exporters import get_exporter
from farapraiser.llm import get_provider
from farapraiser.utils import Config, HardwareDetector
from farapraiser.ui.document_viewer import DocumentViewer


class ParaphraseWorker(QThread):
    """Worker thread for paraphrasing operations."""
    
    progress = pyqtSignal(int, int)  # current, total
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, blocks: List[DocumentBlock], provider, tone: str, num_variants: int):
        super().__init__()
        self.blocks = blocks
        self.provider = provider
        self.tone = tone
        self.num_variants = num_variants
        self.paraphrased_blocks = []
    
    def run(self):
        """Run paraphrasing in background."""
        try:
            total = len(self.blocks)
            for i, block in enumerate(self.blocks):
                text = block.get_text()
                if text.strip():
                    variants = self.provider.paraphrase(text, self.tone, self.num_variants)
                    block.metadata['paraphrased_variants'] = variants
                    block.metadata['selected_variant'] = 0  # Default to original
                
                self.progress.emit(i + 1, total)
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.config = Config()
        self.blocks: List[DocumentBlock] = []
        self.current_file: Optional[str] = None
        self.llm_provider = None
        
        self.init_ui()
        self.init_llm()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("FaraPraiser - AI-Powered Paraphrasing")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create control panel
        control_layout = QHBoxLayout()
        
        # Tone selection
        control_layout.addWidget(QLabel("Tone:"))
        self.tone_combo = QComboBox()
        self.tone_combo.addItems(self.config.get("tones", ["formal", "academic", "casual", "technical", "simplified"]))
        control_layout.addWidget(self.tone_combo)
        
        # Number of variants
        control_layout.addWidget(QLabel("Variants:"))
        self.variants_spin = QSpinBox()
        self.variants_spin.setMinimum(1)
        self.variants_spin.setMaximum(10)
        self.variants_spin.setValue(3)
        control_layout.addWidget(self.variants_spin)
        
        # Paraphrase button
        self.paraphrase_btn = QPushButton("Generate Paraphrases")
        self.paraphrase_btn.clicked.connect(self.start_paraphrasing)
        self.paraphrase_btn.setEnabled(False)
        control_layout.addWidget(self.paraphrase_btn)
        
        control_layout.addStretch()
        layout.addLayout(control_layout)
        
        # Document viewer
        self.document_viewer = DocumentViewer()
        layout.addWidget(self.document_viewer)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status("Ready")
    
    def create_toolbar(self):
        """Create application toolbar."""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # Export action
        self.export_action = QAction("Export", self)
        self.export_action.triggered.connect(self.export_document)
        self.export_action.setEnabled(False)
        toolbar.addAction(self.export_action)
        
        toolbar.addSeparator()
        
        # Settings action
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
        
        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        toolbar.addAction(about_action)
    
    def init_llm(self):
        """Initialize LLM provider."""
        try:
            provider_type = self.config.get("llm.provider", "ollama")
            
            if provider_type == "ollama":
                url = self.config.get("llm.ollama_url")
                model = self.config.get("llm.model")
                if model == "auto":
                    model = HardwareDetector.recommend_model()
                    self.config.set("llm.model", model)
                
                self.llm_provider = get_provider("ollama", base_url=url, model=model)
            
            elif provider_type == "lmstudio":
                url = self.config.get("llm.lmstudio_url")
                model = self.config.get("llm.model", "local-model")
                self.llm_provider = get_provider("lmstudio", base_url=url, model=model)
            
            # Check availability
            if self.llm_provider and self.llm_provider.is_available():
                self.update_status(f"LLM Provider ({provider_type}) connected")
            else:
                self.update_status(f"Warning: LLM Provider ({provider_type}) not available")
                QMessageBox.warning(
                    self,
                    "LLM Not Available",
                    f"Could not connect to {provider_type}. Please make sure it's running.\n\n"
                    f"Ollama: {self.config.get('llm.ollama_url')}\n"
                    f"LM Studio: {self.config.get('llm.lmstudio_url')}"
                )
        
        except Exception as e:
            self.update_status(f"Error initializing LLM: {e}")
            QMessageBox.critical(self, "Error", f"Failed to initialize LLM: {e}")
    
    def open_file(self):
        """Open a document file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Document",
            "",
            "Documents (*.docx *.pdf);;Word Documents (*.docx);;PDF Files (*.pdf)"
        )
        
        if file_path:
            self.load_document(file_path)
    
    def load_document(self, file_path: str):
        """Load and parse a document."""
        try:
            self.update_status(f"Loading {os.path.basename(file_path)}...")
            
            parser = get_parser(file_path)
            self.blocks = parser.parse(file_path)
            self.current_file = file_path
            
            self.document_viewer.set_blocks(self.blocks)
            self.paraphrase_btn.setEnabled(True)
            self.export_action.setEnabled(True)
            
            self.update_status(f"Loaded {len(self.blocks)} blocks from {os.path.basename(file_path)}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load document: {e}")
            self.update_status("Error loading document")
    
    def start_paraphrasing(self):
        """Start paraphrasing process."""
        if not self.llm_provider:
            QMessageBox.warning(self, "No LLM", "LLM provider not available")
            return
        
        if not self.llm_provider.is_available():
            QMessageBox.warning(
                self,
                "LLM Not Available",
                "Cannot connect to LLM provider. Please make sure it's running."
            )
            return
        
        tone = self.tone_combo.currentText()
        num_variants = self.variants_spin.value()
        
        # Disable controls
        self.paraphrase_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Start worker thread
        self.worker = ParaphraseWorker(self.blocks, self.llm_provider, tone, num_variants)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.paraphrasing_finished)
        self.worker.error.connect(self.paraphrasing_error)
        self.worker.start()
        
        self.update_status("Generating paraphrases...")
    
    def update_progress(self, current: int, total: int):
        """Update progress bar."""
        progress = int((current / total) * 100)
        self.progress_bar.setValue(progress)
        self.update_status(f"Processing block {current}/{total}...")
    
    def paraphrasing_finished(self):
        """Handle paraphrasing completion."""
        self.progress_bar.setVisible(False)
        self.paraphrase_btn.setEnabled(True)
        self.document_viewer.refresh()
        self.update_status("Paraphrasing complete")
        QMessageBox.information(self, "Success", "Paraphrasing completed successfully!")
    
    def paraphrasing_error(self, error_msg: str):
        """Handle paraphrasing error."""
        self.progress_bar.setVisible(False)
        self.paraphrase_btn.setEnabled(True)
        self.update_status("Error during paraphrasing")
        QMessageBox.critical(self, "Error", f"Paraphrasing failed: {error_msg}")
    
    def export_document(self):
        """Export the document."""
        if not self.blocks:
            QMessageBox.warning(self, "No Document", "No document loaded")
            return
        
        # Get export format
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Document",
            "",
            "Word Document (*.docx);;PDF File (*.pdf)"
        )
        
        if file_path:
            try:
                # Determine format from extension
                if file_path.lower().endswith('.pdf'):
                    format_type = 'pdf'
                else:
                    format_type = 'docx'
                    if not file_path.lower().endswith('.docx'):
                        file_path += '.docx'
                
                # Create blocks with selected variants
                export_blocks = []
                for block in self.blocks:
                    new_block = DocumentBlock(
                        block_type=block.block_type,
                        content=block.content,
                        metadata=block.metadata.copy(),
                        index=block.index
                    )
                    
                    # Use selected variant if available
                    if 'paraphrased_variants' in block.metadata:
                        selected_idx = block.metadata.get('selected_variant', 0)
                        variants = block.metadata['paraphrased_variants']
                        if selected_idx > 0 and variants and selected_idx - 1 < len(variants):
                            new_block.content = variants[selected_idx - 1]
                    
                    export_blocks.append(new_block)
                
                exporter = get_exporter(format_type)
                exporter.export(export_blocks, file_path)
                
                self.update_status(f"Exported to {os.path.basename(file_path)}")
                QMessageBox.information(self, "Success", f"Document exported to {file_path}")
            
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export document: {e}")
                self.update_status("Error exporting document")
    
    def show_settings(self):
        """Show settings dialog."""
        # Simple info dialog for now
        info = HardwareDetector.get_system_info()
        recommended = HardwareDetector.recommend_model()
        
        msg = f"""System Information:
Platform: {info['platform']}
Processor: {info['processor']}
RAM: {info['ram_gb']:.1f} GB
CPU Cores: {info['cpu_count']}
CPU Threads: {info['cpu_threads']}

Recommended Model: {recommended}

Current LLM Provider: {self.config.get('llm.provider')}
Model: {self.config.get('llm.model')}

Configuration file: {self.config.config_file}
"""
        QMessageBox.information(self, "Settings", msg)
    
    def show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About FaraPraiser",
            "<h2>FaraPraiser v0.1.0</h2>"
            "<p>Offline AI-powered academic paraphrasing app with DOCX/PDF parsing, "
            "table-safe editing, and local LLM support.</p>"
            "<p>Built for thesis & research workflows.</p>"
            "<p>Uses PyQt6, python-docx, PyPDF2, and local LLMs (Ollama/LM Studio)</p>"
        )
    
    def update_status(self, message: str):
        """Update status bar message."""
        self.status_bar.showMessage(message)
