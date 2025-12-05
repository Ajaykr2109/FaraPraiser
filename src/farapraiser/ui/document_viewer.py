"""Document viewer widget with paraphrase variants and diff view."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel,
    QPushButton, QComboBox, QTextEdit, QFrame, QSplitter
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import List, Optional
import difflib

from farapraiser.parsers.base import DocumentBlock, BlockType


class BlockWidget(QFrame):
    """Widget representing a single document block."""
    
    def __init__(self, block: DocumentBlock, parent=None):
        super().__init__(parent)
        self.block = block
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(1)
        
        layout = QVBoxLayout(self)
        
        # Header with block type and index
        header_layout = QHBoxLayout()
        
        type_label = QLabel(f"[{self.block.block_type.value.upper()}]")
        type_label.setStyleSheet("font-weight: bold; color: #0066cc;")
        header_layout.addWidget(type_label)
        
        index_label = QLabel(f"Block #{self.block.index + 1}")
        index_label.setStyleSheet("color: #666;")
        header_layout.addWidget(index_label)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Original content
        original_label = QLabel("Original:")
        original_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(original_label)
        
        self.original_text = QTextEdit()
        self.original_text.setPlainText(self.block.get_text())
        self.original_text.setReadOnly(True)
        self.original_text.setMaximumHeight(100)
        layout.addWidget(self.original_text)
        
        # Paraphrased variants section
        variants_layout = QHBoxLayout()
        
        variant_label = QLabel("Select variant:")
        variants_layout.addWidget(variant_label)
        
        self.variant_combo = QComboBox()
        self.variant_combo.addItem("Original")
        self.variant_combo.currentIndexChanged.connect(self.on_variant_changed)
        variants_layout.addWidget(self.variant_combo)
        
        self.diff_btn = QPushButton("Show Diff")
        self.diff_btn.clicked.connect(self.show_diff)
        self.diff_btn.setEnabled(False)
        variants_layout.addWidget(self.diff_btn)
        
        variants_layout.addStretch()
        layout.addLayout(variants_layout)
        
        # Paraphrased text display
        self.paraphrased_text = QTextEdit()
        self.paraphrased_text.setReadOnly(True)
        self.paraphrased_text.setMaximumHeight(100)
        self.paraphrased_text.setVisible(False)
        layout.addWidget(self.paraphrased_text)
        
        # Diff view
        self.diff_text = QTextEdit()
        self.diff_text.setReadOnly(True)
        self.diff_text.setMaximumHeight(150)
        self.diff_text.setVisible(False)
        font = QFont("Courier")
        font.setPointSize(9)
        self.diff_text.setFont(font)
        layout.addWidget(self.diff_text)
        
        self.update_variants()
    
    def update_variants(self):
        """Update the variants combo box."""
        variants = self.block.metadata.get('paraphrased_variants', [])
        
        # Clear existing items except "Original"
        while self.variant_combo.count() > 1:
            self.variant_combo.removeItem(1)
        
        # Add variants
        for i, variant in enumerate(variants, 1):
            self.variant_combo.addItem(f"Variant {i}")
        
        # Enable/disable diff button
        self.diff_btn.setEnabled(len(variants) > 0)
        
        # Set selected variant
        selected = self.block.metadata.get('selected_variant', 0)
        if selected < self.variant_combo.count():
            self.variant_combo.setCurrentIndex(selected)
    
    def on_variant_changed(self, index: int):
        """Handle variant selection change."""
        self.block.metadata['selected_variant'] = index
        
        if index == 0:
            # Original selected
            self.paraphrased_text.setVisible(False)
            self.diff_text.setVisible(False)
        else:
            # Variant selected
            variants = self.block.metadata.get('paraphrased_variants', [])
            if index - 1 < len(variants):
                self.paraphrased_text.setPlainText(variants[index - 1])
                self.paraphrased_text.setVisible(True)
                
                # Update diff if it was visible
                if self.diff_text.isVisible():
                    self.show_diff()
    
    def show_diff(self):
        """Show diff between original and selected variant."""
        selected_idx = self.variant_combo.currentIndex()
        
        if selected_idx == 0:
            self.diff_text.setVisible(False)
            return
        
        variants = self.block.metadata.get('paraphrased_variants', [])
        if selected_idx - 1 >= len(variants):
            return
        
        original = self.block.get_text()
        variant = variants[selected_idx - 1]
        
        # Generate diff
        diff = self.generate_diff(original, variant)
        self.diff_text.setHtml(diff)
        self.diff_text.setVisible(True)
    
    def generate_diff(self, text1: str, text2: str) -> str:
        """Generate HTML diff between two texts."""
        # Split into lines for better diff
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        diff = difflib.unified_diff(lines1, lines2, lineterm='', n=0)
        
        html_parts = ['<pre style="font-family: monospace; font-size: 10pt;">']
        
        for line in diff:
            if line.startswith('---') or line.startswith('+++'):
                continue
            elif line.startswith('@@'):
                html_parts.append(f'<span style="color: #0066cc;">{line}</span><br>')
            elif line.startswith('-'):
                html_parts.append(f'<span style="background-color: #ffcccc; color: #cc0000;">{line}</span><br>')
            elif line.startswith('+'):
                html_parts.append(f'<span style="background-color: #ccffcc; color: #00cc00;">{line}</span><br>')
            else:
                html_parts.append(f'{line}<br>')
        
        html_parts.append('</pre>')
        
        if len(html_parts) == 2:  # Only pre tags, no actual diff
            return '<p><i>Texts are identical</i></p>'
        
        return ''.join(html_parts)
    
    def refresh(self):
        """Refresh the widget display."""
        self.update_variants()


class DocumentViewer(QWidget):
    """Scrollable viewer for document blocks."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks: List[DocumentBlock] = []
        self.block_widgets: List[BlockWidget] = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Container widget for blocks
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setSpacing(10)
        
        self.scroll_area.setWidget(self.container)
        layout.addWidget(self.scroll_area)
    
    def set_blocks(self, blocks: List[DocumentBlock]):
        """Set the document blocks to display."""
        self.blocks = blocks
        self.render_blocks()
    
    def render_blocks(self):
        """Render all document blocks."""
        # Clear existing widgets
        for widget in self.block_widgets:
            widget.deleteLater()
        self.block_widgets.clear()
        
        # Create new widgets for each block
        for block in self.blocks:
            widget = BlockWidget(block)
            self.block_widgets.append(widget)
            self.container_layout.addWidget(widget)
        
        # Add stretch at the end
        self.container_layout.addStretch()
    
    def refresh(self):
        """Refresh all block widgets."""
        for widget in self.block_widgets:
            widget.refresh()
