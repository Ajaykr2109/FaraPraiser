# FaraPraiser Quick Start Guide

## Prerequisites

1. **Install Python 3.8+** from https://www.python.org/downloads/

2. **Install a Local LLM Provider** (choose one):

   ### Option A: Ollama (Recommended)
   ```bash
   # Visit https://ollama.ai and download installer
   # After installation, open terminal and run:
   ollama pull llama2
   # Or for smaller systems:
   ollama pull phi
   
   # Start Ollama:
   ollama serve
   ```

   ### Option B: LM Studio
   ```bash
   # Download from https://lmstudio.ai
   # Install and load a model
   # Start the local server (Menu: Local Server → Start)
   ```

## Installation

```bash
# Clone repository
git clone https://github.com/Ajaykr2109/FaraPraiser.git
cd FaraPraiser

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

## Running FaraPraiser

```bash
# Method 1: Using command
farapraiser

# Method 2: Using Python
python run.py

# Method 3: Direct execution
python src/farapraiser/main.py
```

## First-Time Setup

1. **Verify LLM Connection**: Check status bar when app starts
2. **Try Sample Document**: Open `resources/sample_document.docx`
3. **Generate Paraphrases**: 
   - Select tone (e.g., "academic")
   - Set variants to 3
   - Click "Generate Paraphrases"
4. **Review Results**: Select variants and use "Show Diff"
5. **Export**: Click "Export" and choose format

## Troubleshooting

### "LLM Provider not available"
- Ensure Ollama is running: `ollama serve`
- Or check LM Studio server is started
- Verify URLs in Settings:
  - Ollama: http://localhost:11434
  - LM Studio: http://localhost:1234

### "No module named 'farapraiser'"
```bash
pip install -e .
```

### Slow Performance
- Use smaller model: `ollama pull phi`
- Reduce number of variants
- Check hardware with Settings button

### Import Errors
```bash
pip install -r requirements.txt
```

## Quick Tips

- **Best Results**: Use academic tone for research papers
- **Multiple Variants**: 3-5 variants provide good variety
- **Diff View**: Shows exactly what changed
- **Tables**: Preserved in exported documents
- **Batch Edit**: Process multiple blocks at once

## Sample Workflow

1. Start Ollama: `ollama serve`
2. Launch app: `farapraiser`
3. Open document: Toolbar → Open
4. Configure: Tone = academic, Variants = 3
5. Generate: Click "Generate Paraphrases"
6. Review: Select variants, view diffs
7. Export: Toolbar → Export → Choose DOCX/PDF

## Configuration

Edit `~/.farapraiser/config.json` to customize:
- LLM provider and model
- UI preferences
- Export settings
- Custom tones

## Getting Help

- Check README.md for detailed documentation
- Review system info in Settings
- Open issues on GitHub

## Sample Documents

Try the included sample:
```bash
resources/sample_document.docx  # Example academic document
```

Happy Paraphrasing! 🎉
