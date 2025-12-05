"""Document exporters for DOCX and PDF."""

from abc import ABC, abstractmethod
from typing import List
from farapraiser.parsers.base import DocumentBlock


class DocumentExporter(ABC):
    """Abstract base class for document exporters."""
    
    @abstractmethod
    def export(self, blocks: List[DocumentBlock], output_path: str) -> None:
        """Export blocks to a document file."""
        pass
