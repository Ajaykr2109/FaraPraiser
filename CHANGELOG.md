# Changelog

All notable changes to FaraPraiser will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-12-05

### Added
- Initial release of FaraPraiser
- Complete PyQt6-based GUI application
- DOCX document parser with support for paragraphs, tables, lists, and headings
- PDF document parser with text extraction
- Ollama LLM provider integration
- LM Studio LLM provider integration
- Multiple paraphrase variant generation (1-10 variants)
- Tone selection (formal, academic, casual, technical, simplified)
- Interactive diff view with color-coded changes
- DOCX exporter with formatting preservation
- PDF exporter using ReportLab
- Hardware detection and automatic model recommendation
- JSON-based configuration system
- Progress tracking for batch operations
- Status bar for user feedback
- Comprehensive README with installation and usage instructions
- Quick start guide (QUICKSTART.md)
- Architecture documentation (ARCHITECTURE.md)
- Feature list (FEATURES.md)
- Unit tests for core functionality
- Sample documents for testing
- Demo script to showcase functionality
- MIT License
- .gitignore for Python projects
- Setup.py for package installation
- Requirements.txt with all dependencies

### Features
- Load and parse DOCX and PDF documents
- Extract document blocks (paragraphs, tables, lists, headings)
- Generate multiple paraphrased variants using local LLMs
- Select from different tones (formal, academic, casual, technical, simplified)
- View side-by-side comparison with diff highlighting
- Export results to DOCX or PDF with selected variants
- Automatic hardware detection and model recommendation
- User-friendly GUI with scrollable document viewer
- Background processing with progress indicators
- Configurable settings via JSON file

### Technical Details
- Python 3.8+ support
- PyQt6 for GUI
- python-docx for DOCX handling
- PyPDF2 for PDF reading
- ReportLab for PDF generation
- Requests for LLM API communication
- psutil for hardware detection
- Modular architecture with clear separation of concerns
- Abstract base classes for extensibility
- Factory pattern for parser/exporter selection
- Threading for responsive UI
- Comprehensive error handling

### Documentation
- Complete README with installation, usage, and troubleshooting
- Quick start guide for new users
- Architecture documentation for developers
- Comprehensive feature list
- Inline code documentation with docstrings
- Sample documents for testing

### Testing
- Unit tests for configuration management
- Unit tests for hardware detection
- Unit tests for document blocks
- Unit tests for LLM providers (with mocking)
- Demo script for manual testing
- Sample documents for integration testing

## [Unreleased]

### Planned Features
- Batch file processing
- Custom paraphrase templates
- Keyboard shortcuts
- Undo/redo functionality
- Dark theme support
- Translation support
- Additional input formats (RTF, TXT, HTML)
- Document comparison mode
- Plugin system for extensibility
- Cloud LLM support (optional)

### Known Issues
- PDF table extraction is limited (text only)
- Complex document formatting may be simplified on export
- Sequential LLM processing (not parallel)
- Single document processing at a time

---

## Version History

- **0.1.0** (2024-12-05): Initial release with core functionality

## Notes

### Versioning Strategy
- **Major version** (X.0.0): Breaking changes, major feature additions
- **Minor version** (0.X.0): New features, backwards compatible
- **Patch version** (0.0.X): Bug fixes, minor improvements

### Release Schedule
- Feature releases: As features are completed
- Bug fix releases: As needed
- Security releases: Immediately upon discovery

### Support Policy
- Current version: Full support
- Previous minor version: Security fixes only
- Older versions: No support (upgrade recommended)
