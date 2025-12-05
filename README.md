# FaraPraiser

Offline AI-powered academic paraphrasing app with DOCX/PDF parsing, table-safe editing, and local LLM support — built for thesis & research workflows.

## Features

- **Document Loading**: Support for DOCX and PDF files
- **Smart Parsing**: Extracts paragraphs, tables, lists, and headings
- **AI Paraphrasing**: Generate multiple paraphrased variants using local LLMs
- **Tone Options**: Choose from formal, academic, casual, technical, or simplified tones
- **Diff View**: Visual comparison between original and paraphrased text
- **Hardware Detection**: Automatically recommends optimal LLM model based on your system
- **Export Options**: Save results as DOCX or PDF
- **Privacy-First**: All processing happens locally with no internet required (except for downloading models)

## Prerequisites

### System Requirements

- Python 3.8 or higher
- 4GB RAM minimum (8GB+ recommended)
- Windows, macOS, or Linux

### LLM Provider (Choose One)

You need to install and run one of these local LLM providers:

#### Option 1: Ollama (Recommended)
```bash
# Install Ollama from https://ollama.ai
# Then pull a model:
ollama pull llama2
# or for smaller systems:
ollama pull phi
```

#### Option 2: LM Studio
- Download and install from https://lmstudio.ai
- Load a model in LM Studio
- Start the local server (default: http://localhost:1234)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Ajaykr2109/FaraPraiser.git
cd FaraPraiser
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install the Package
```bash
pip install -e .
```

## Usage

### Starting the Application

#### Method 1: Using the command
```bash
farapraiser
```

#### Method 2: Using Python
```bash
python src/farapraiser/main.py
```

### Workflow

1. **Start your LLM provider** (Ollama or LM Studio)
   ```bash
   # For Ollama:
   ollama serve
   ```

2. **Open FaraPraiser** and verify LLM connection in the status bar

3. **Load a Document**:
   - Click "Open" in the toolbar
   - Select a DOCX or PDF file

4. **Configure Paraphrasing**:
   - Choose a tone (formal, academic, casual, technical, simplified)
   - Set number of variants (1-10)

5. **Generate Paraphrases**:
   - Click "Generate Paraphrases"
   - Wait for processing (shown in progress bar)

6. **Review Results**:
   - Each block shows the original text
   - Select different variants from the dropdown
   - Click "Show Diff" to see changes

7. **Export**:
   - Click "Export" in the toolbar
   - Choose DOCX or PDF format
   - Selected variants will be included in the export

## Configuration

Configuration is stored in `~/.farapraiser/config.json`

### Default Configuration
```json
{
  "llm": {
    "provider": "ollama",
    "ollama_url": "http://localhost:11434",
    "lmstudio_url": "http://localhost:1234/v1",
    "model": "auto",
    "timeout": 60,
    "max_tokens": 1024
  },
  "ui": {
    "theme": "light",
    "font_size": 11,
    "max_variants": 5
  },
  "export": {
    "default_format": "docx",
    "include_metadata": true
  },
  "tones": [
    "formal",
    "academic",
    "casual",
    "technical",
    "simplified"
  ]
}
```

### Customizing

Edit `~/.farapraiser/config.json` to:
- Change LLM provider URLs
- Set a specific model instead of auto-detection
- Adjust timeout values
- Add custom tones

## Hardware Recommendations

The app automatically detects your hardware and recommends an appropriate model:

| RAM | GPU | Recommended Model |
|-----|-----|-------------------|
| 16GB+ | Yes | llama2:13b |
| 8GB+ | No | llama2:7b |
| 4GB+ | No | phi |
| <4GB | No | tinyllama |

You can override this by setting `"model"` in the config file.

## Project Structure

```
FaraPraiser/
├── src/farapraiser/
│   ├── main.py              # Entry point
│   ├── ui/
│   │   ├── main_window.py   # Main application window
│   │   └── document_viewer.py # Document display widget
│   ├── parsers/
│   │   ├── base.py          # Parser interface
│   │   ├── docx_parser.py   # DOCX parser
│   │   └── pdf_parser.py    # PDF parser
│   ├── llm/
│   │   └── providers.py     # LLM integration (Ollama/LM Studio)
│   ├── exporters/
│   │   ├── docx_exporter.py # DOCX exporter
│   │   └── pdf_exporter.py  # PDF exporter
│   └── utils/
│       ├── config.py        # Configuration management
│       └── hardware.py      # Hardware detection
├── tests/                   # Test files
├── resources/               # Resources (icons, etc.)
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
└── README.md               # This file
```

## Troubleshooting

### LLM Provider Not Available
- Ensure Ollama or LM Studio is running
- Check the URLs in settings (Ollama: http://localhost:11434, LM Studio: http://localhost:1234)
- Verify model is downloaded: `ollama list` or check LM Studio

### Document Loading Issues
- Ensure file is a valid DOCX or PDF
- Check file permissions
- Try a different document

### Out of Memory
- Use a smaller model (phi or tinyllama)
- Reduce number of variants
- Process smaller documents

### Slow Performance
- Check hardware recommendations
- Ensure LLM provider is using GPU if available
- Reduce timeout in config
- Close other applications

## Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
# Format code
black src/

# Check style
flake8 src/
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Acknowledgments

- PyQt6 for the GUI framework
- python-docx for DOCX handling
- PyPDF2 for PDF parsing
- Ollama and LM Studio for local LLM inference
- ReportLab for PDF generation

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

## Roadmap

- [ ] Support for more document formats (RTF, TXT, HTML)
- [ ] Batch processing
- [ ] Custom paraphrasing templates
- [ ] Translation support
- [ ] Cloud LLM providers (optional)
- [ ] Plugin system
- [ ] Dark theme
- [ ] Advanced diff visualization
