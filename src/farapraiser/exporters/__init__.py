"""Exporters package."""

from farapraiser.exporters.base import DocumentExporter
from farapraiser.exporters.docx_exporter import DOCXExporter
from farapraiser.exporters.pdf_exporter import PDFExporter

__all__ = ["DocumentExporter", "DOCXExporter", "PDFExporter"]


def get_exporter(format_type: str) -> DocumentExporter:
    """Get appropriate exporter for the given format."""
    exporters = {
        "docx": DOCXExporter(),
        "pdf": PDFExporter(),
    }
    
    exporter = exporters.get(format_type.lower())
    if not exporter:
        raise ValueError(f"No exporter found for format: {format_type}")
    
    return exporter
