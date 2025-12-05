"""Document parsers package."""

from farapraiser.parsers.base import DocumentParser, DocumentBlock, BlockType
from farapraiser.parsers.docx_parser import DOCXParser
from farapraiser.parsers.pdf_parser import PDFParser

__all__ = ["DocumentParser", "DocumentBlock", "BlockType", "DOCXParser", "PDFParser"]


def get_parser(file_path: str) -> DocumentParser:
    """Get appropriate parser for the given file."""
    parsers = [DOCXParser(), PDFParser()]
    
    for parser in parsers:
        if parser.supports_format(file_path):
            return parser
    
    raise ValueError(f"No parser found for file: {file_path}")
