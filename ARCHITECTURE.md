# FaraPraiser Architecture Documentation

## System Architecture

FaraPraiser follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface (PyQt6)                  │
│  ┌─────────────────┐        ┌──────────────────────┐       │
│  │  Main Window    │        │  Document Viewer     │       │
│  │  - File ops     │   ←→   │  - Block display     │       │
│  │  - Controls     │        │  - Variant selection │       │
│  │  - Status       │        │  - Diff view         │       │
│  └─────────────────┘        └──────────────────────┘       │
└──────────────────┬──────────────────────┬──────────────────┘
                   │                      │
                   ↓                      ↓
┌──────────────────────────┐   ┌─────────────────────────────┐
│   Document Parsers       │   │    LLM Integration          │
│   - DOCX Parser          │   │    - Ollama Provider        │
│   - PDF Parser           │   │    - LM Studio Provider     │
│   - Block extraction     │   │    - Paraphrase generation  │
└──────────────────────────┘   └─────────────────────────────┘
           ↓                              ↓
┌──────────────────────────┐   ┌─────────────────────────────┐
│   Document Exporters     │   │    Utilities                │
│   - DOCX Exporter        │   │    - Config Management      │
│   - PDF Exporter         │   │    - Hardware Detection     │
│   - Format conversion    │   │    - Model Selection        │
└──────────────────────────┘   └─────────────────────────────┘
```

## Component Details

### 1. User Interface Layer (`ui/`)

#### Main Window (`main_window.py`)
- **Responsibilities**: 
  - Application lifecycle management
  - File operations (open/export)
  - LLM provider initialization
  - User controls for paraphrasing
  - Progress tracking
  - Settings and about dialogs

- **Key Features**:
  - Toolbar with file operations
  - Tone selection dropdown
  - Variant count spinner
  - Progress bar for batch processing
  - Status bar for user feedback

#### Document Viewer (`document_viewer.py`)
- **Responsibilities**:
  - Display document blocks in scrollable view
  - Manage block widgets
  - Handle variant selection
  - Generate and display diffs

- **Key Features**:
  - Block-level display with metadata
  - Original/paraphrased text comparison
  - Variant dropdown per block
  - Color-coded diff visualization
  - Responsive scrolling

### 2. Document Processing Layer

#### Parsers (`parsers/`)
- **Base Parser** (`base.py`):
  - Abstract interface for parsers
  - `DocumentBlock` data structure
  - `BlockType` enumeration

- **DOCX Parser** (`docx_parser.py`):
  - Extracts paragraphs, tables, lists, headings
  - Preserves document structure and styles
  - Maintains element order

- **PDF Parser** (`pdf_parser.py`):
  - Text extraction from PDF pages
  - Simple list detection heuristics
  - Page metadata tracking

#### Exporters (`exporters/`)
- **Base Exporter** (`base.py`):
  - Abstract interface for exporters

- **DOCX Exporter** (`docx_exporter.py`):
  - Reconstructs DOCX with selected variants
  - Preserves tables and formatting
  - Applies appropriate styles

- **PDF Exporter** (`pdf_exporter.py`):
  - Generates PDF using ReportLab
  - Creates structured layout
  - Handles tables and lists

### 3. LLM Integration Layer (`llm/`)

#### Providers (`providers.py`)
- **Base Provider**:
  - Abstract interface for LLM providers
  - Common prompt building logic
  - Tone-specific instructions

- **Ollama Provider**:
  - REST API integration with Ollama
  - Availability checking
  - Streaming support (disabled for reliability)
  - Temperature variation for diversity

- **LM Studio Provider**:
  - OpenAI-compatible API integration
  - Chat completions endpoint
  - Similar paraphrasing logic

### 4. Utilities Layer (`utils/`)

#### Configuration (`config.py`)
- JSON-based configuration
- Default settings
- Deep merge for user overrides
- Auto-save functionality
- Dot-notation access

#### Hardware Detection (`hardware.py`)
- System information gathering
- GPU detection (NVIDIA via nvidia-smi)
- RAM and CPU analysis
- Model recommendations based on hardware
- Thread optimization

## Data Flow

### Document Loading Flow
```
User selects file
    ↓
MainWindow.open_file()
    ↓
get_parser(file_path)
    ↓
parser.parse() → List[DocumentBlock]
    ↓
DocumentViewer.set_blocks()
    ↓
Render BlockWidget for each block
```

### Paraphrasing Flow
```
User clicks "Generate Paraphrases"
    ↓
MainWindow.start_paraphrasing()
    ↓
Create ParaphraseWorker thread
    ↓
For each block:
    - Extract text with block.get_text()
    - Call provider.paraphrase(text, tone, num_variants)
    - Store variants in block.metadata
    ↓
Update UI with variants
    ↓
User selects variants per block
```

### Export Flow
```
User clicks "Export"
    ↓
MainWindow.export_document()
    ↓
Create export blocks with selected variants
    ↓
get_exporter(format)
    ↓
exporter.export(blocks, output_path)
    ↓
Save file to disk
```

## Design Patterns

### 1. Strategy Pattern
- Used in parsers and exporters
- Abstract base classes define interface
- Concrete implementations for different formats

### 2. Factory Pattern
- `get_parser()` returns appropriate parser
- `get_exporter()` returns appropriate exporter
- `get_provider()` returns LLM provider

### 3. Observer Pattern
- Qt signals/slots for UI updates
- Worker thread progress signals
- Event-driven architecture

### 4. Data Class Pattern
- `DocumentBlock` encapsulates block data
- Metadata dictionary for extensibility
- Type-safe with dataclasses

## Threading Model

- **Main Thread**: UI operations, user interaction
- **Worker Thread**: LLM paraphrasing (CPU/network intensive)
- **Signals**: Safe cross-thread communication

## Error Handling

### Graceful Degradation
- LLM unavailable → warning message, app still functional
- Parse error → show error, allow retry
- Export error → show error, keep working document

### User Feedback
- Status bar for all operations
- Progress bar for long operations
- Message boxes for important events
- Console logging for debugging

## Configuration Architecture

### Hierarchy
1. Default configuration (hardcoded)
2. User configuration (~/.farapraiser/config.json)
3. Runtime overrides (if any)

### Extensibility
- New tones: add to config.tones array
- New models: set llm.model
- Custom URLs: modify llm.*_url

## Testing Strategy

### Unit Tests
- Config management
- Hardware detection
- Document block operations
- LLM provider mocking

### Integration Tests
- Document parsing (real files)
- Export functionality
- End-to-end workflows

### Manual Testing
- UI interactions
- LLM integration (requires running service)
- Cross-platform compatibility

## Dependencies

### Core Dependencies
- **PyQt6**: GUI framework
- **python-docx**: DOCX manipulation
- **PyPDF2**: PDF reading
- **reportlab**: PDF generation
- **requests**: HTTP client for LLM APIs
- **psutil**: System information

### Development Dependencies
- **pytest**: Testing framework
- **unittest.mock**: Mocking for tests

## Performance Considerations

### Optimization Strategies
1. **Lazy Loading**: Only parse when needed
2. **Threading**: Background paraphrasing
3. **Caching**: Store variants in metadata
4. **Batch Processing**: Process all blocks together
5. **Memory Management**: Clear unused widgets

### Scalability
- Handles documents up to ~1000 blocks efficiently
- Memory usage scales with document size
- LLM calls are sequential (can be parallelized)

## Security Considerations

1. **Local Processing**: No data sent to cloud
2. **User Privacy**: All LLM inference local
3. **File Safety**: No destructive operations on originals
4. **Configuration**: Plain text, user-editable

## Future Enhancements

### Planned Features
- [ ] Batch document processing
- [ ] Custom paraphrase templates
- [ ] Translation support
- [ ] Cloud LLM providers (optional)
- [ ] Plugin system for custom parsers
- [ ] Dark theme
- [ ] Keyboard shortcuts
- [ ] Undo/redo functionality
- [ ] Document comparison mode
- [ ] Export templates

### Architecture Evolution
- Plugin system for extensibility
- Async/await for better concurrency
- Database for large document sets
- Web interface option
- API service mode

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Solution: `pip install -e .`

2. **LLM Connection**
   - Check service is running
   - Verify URL in config
   - Test with `curl`

3. **Memory Issues**
   - Use smaller model
   - Process fewer variants
   - Close other apps

4. **UI Not Responding**
   - Long paraphrasing blocks UI
   - Use smaller documents
   - Reduce timeout

## Development Guidelines

### Code Style
- Follow PEP 8
- Type hints for public APIs
- Docstrings for all modules/classes
- Comments for complex logic

### Adding New Features
1. Create feature branch
2. Write tests first
3. Implement feature
4. Update documentation
5. Submit pull request

### Adding New Parser
1. Extend `DocumentParser`
2. Implement `parse()` and `supports_format()`
3. Add to `get_parser()` factory
4. Write tests
5. Update README

### Adding New Exporter
1. Extend `DocumentExporter`
2. Implement `export()`
3. Add to `get_exporter()` factory
4. Write tests
5. Update README

## Conclusion

FaraPraiser is designed as a modular, extensible application with clear separation of concerns. The architecture supports easy addition of new parsers, exporters, and LLM providers while maintaining stability and user experience.
