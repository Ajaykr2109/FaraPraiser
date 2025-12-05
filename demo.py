#!/usr/bin/env python3
"""
Demo script to showcase FaraPraiser capabilities without GUI.
This demonstrates the core functionality for testing and documentation.
"""

import sys
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from farapraiser.parsers import get_parser
from farapraiser.exporters import get_exporter
from farapraiser.utils import Config, HardwareDetector
from farapraiser.llm import get_provider


def print_section(title):
    """Print a section header."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print('=' * 70)


def demo_system_info():
    """Demonstrate system information and hardware detection."""
    print_section("SYSTEM INFORMATION")
    
    info = HardwareDetector.get_system_info()
    print(f"Platform: {info['platform']}")
    print(f"Processor: {info['processor']}")
    print(f"RAM: {info['ram_gb']:.2f} GB")
    print(f"CPU Cores: {info['cpu_count']} physical, {info['cpu_threads']} threads")
    print(f"GPU Available: {HardwareDetector.has_gpu()}")
    print(f"\nRecommended Model: {HardwareDetector.recommend_model()}")
    print(f"Optimal Threads: {HardwareDetector.get_optimal_threads()}")


def demo_configuration():
    """Demonstrate configuration management."""
    print_section("CONFIGURATION")
    
    config = Config()
    print(f"LLM Provider: {config.get('llm.provider')}")
    print(f"Model: {config.get('llm.model')}")
    print(f"Ollama URL: {config.get('llm.ollama_url')}")
    print(f"LM Studio URL: {config.get('llm.lmstudio_url')}")
    print(f"\nAvailable Tones: {', '.join(config.get('tones'))}")
    print(f"Max Variants: {config.get('ui.max_variants')}")


def demo_document_parsing():
    """Demonstrate document parsing."""
    print_section("DOCUMENT PARSING")
    
    sample_doc = Path("resources/sample_document.docx")
    
    if not sample_doc.exists():
        print(f"Sample document not found: {sample_doc}")
        return
    
    print(f"Parsing: {sample_doc}")
    parser = get_parser(str(sample_doc))
    blocks = parser.parse(str(sample_doc))
    
    print(f"\nFound {len(blocks)} blocks:")
    print("-" * 70)
    
    for i, block in enumerate(blocks, 1):
        text = block.get_text()
        if len(text) > 60:
            text = text[:60] + "..."
        print(f"\n{i}. Type: {block.block_type.value.upper()}")
        print(f"   Content: {text}")
        print(f"   Metadata: {block.metadata}")


def demo_llm_provider():
    """Demonstrate LLM provider connectivity."""
    print_section("LLM PROVIDER")
    
    config = Config()
    provider_type = config.get('llm.provider')
    
    print(f"Testing {provider_type} provider...")
    
    try:
        if provider_type == "ollama":
            provider = get_provider(
                "ollama",
                base_url=config.get('llm.ollama_url'),
                model=config.get('llm.model')
            )
        else:
            provider = get_provider(
                "lmstudio",
                base_url=config.get('llm.lmstudio_url'),
                model=config.get('llm.model')
            )
        
        is_available = provider.is_available()
        print(f"Provider available: {is_available}")
        
        if is_available:
            print("\nTesting paraphrase generation (this may take a moment)...")
            test_text = "The quick brown fox jumps over the lazy dog."
            variants = provider.paraphrase(test_text, tone="formal", num_variants=1)
            
            if variants:
                print(f"\nOriginal: {test_text}")
                print(f"Paraphrased: {variants[0]}")
            else:
                print("No variants generated (this is expected if LLM is not ready)")
        else:
            print(f"\nNote: {provider_type} is not running.")
            print(f"Start it with:")
            if provider_type == "ollama":
                print("  ollama serve")
            else:
                print("  (Start LM Studio and enable the local server)")
    
    except Exception as e:
        print(f"Error testing LLM provider: {e}")


def demo_export():
    """Demonstrate document export."""
    print_section("DOCUMENT EXPORT")
    
    sample_doc = Path("resources/sample_document.docx")
    
    if not sample_doc.exists():
        print(f"Sample document not found: {sample_doc}")
        return
    
    # Parse document
    parser = get_parser(str(sample_doc))
    blocks = parser.parse(str(sample_doc))
    
    # Add mock paraphrased content to first text block
    for block in blocks:
        text = block.get_text()
        if text and len(text) > 20:
            block.metadata['paraphrased_variants'] = [
                f"[Paraphrased] {text}"
            ]
            block.metadata['selected_variant'] = 1
            break
    
    # Export to both formats
    demo_docx = Path("resources/demo_output.docx")
    demo_pdf = Path("resources/demo_output.pdf")
    
    try:
        exporter = get_exporter('docx')
        exporter.export(blocks, str(demo_docx))
        print(f"✓ Exported to DOCX: {demo_docx}")
        
        exporter = get_exporter('pdf')
        exporter.export(blocks, str(demo_pdf))
        print(f"✓ Exported to PDF: {demo_pdf}")
    
    except Exception as e:
        print(f"Error during export: {e}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print("  FaraPraiser - Core Functionality Demonstration")
    print("=" * 70)
    
    try:
        demo_system_info()
        demo_configuration()
        demo_document_parsing()
        demo_llm_provider()
        demo_export()
        
        print("\n" + "=" * 70)
        print("  Demo Complete!")
        print("=" * 70)
        print("\nTo run the full GUI application:")
        print("  python run.py")
        print("  or: farapraiser")
        print()
    
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
