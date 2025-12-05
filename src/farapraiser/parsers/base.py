"""Document parsers for DOCX and PDF files."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum


class BlockType(Enum):
    """Types of document blocks."""
    PARAGRAPH = "paragraph"
    TABLE = "table"
    LIST = "list"
    HEADING = "heading"


@dataclass
class DocumentBlock:
    """Represents a block of content from a document."""
    block_type: BlockType
    content: Any
    metadata: Dict[str, Any]
    index: int
    
    def get_text(self) -> str:
        """Get text representation of the block."""
        if self.block_type == BlockType.PARAGRAPH:
            return self.content
        elif self.block_type == BlockType.LIST:
            return "\n".join(f"• {item}" for item in self.content)
        elif self.block_type == BlockType.TABLE:
            # Simple table representation
            rows = []
            for row in self.content:
                rows.append(" | ".join(str(cell) for cell in row))
            return "\n".join(rows)
        elif self.block_type == BlockType.HEADING:
            return self.content
        return str(self.content)


class DocumentParser(ABC):
    """Abstract base class for document parsers."""
    
    @abstractmethod
    def parse(self, file_path: str) -> List[DocumentBlock]:
        """Parse document and return list of blocks."""
        pass
    
    @abstractmethod
    def supports_format(self, file_path: str) -> bool:
        """Check if parser supports the given file format."""
        pass
