"""PDF document parser."""

from typing import List
import PyPDF2
from farapraiser.parsers.base import DocumentParser, DocumentBlock, BlockType


class PDFParser(DocumentParser):
    """Parser for PDF files."""
    
    def supports_format(self, file_path: str) -> bool:
        """Check if file is PDF format."""
        return file_path.lower().endswith('.pdf')
    
    def parse(self, file_path: str) -> List[DocumentBlock]:
        """Parse PDF file and extract text blocks."""
        blocks = []
        index = 0
        
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                
                if not text.strip():
                    continue
                
                # Split into paragraphs (simple approach)
                paragraphs = text.split('\n\n')
                
                for para_text in paragraphs:
                    para_text = para_text.strip()
                    if para_text:
                        # Try to detect lists (simple heuristic)
                        lines = para_text.split('\n')
                        if len(lines) > 1 and all(
                            line.strip().startswith(('•', '-', '*', '◦')) or 
                            (len(line) > 0 and line[0].isdigit() and len(line) > 1 and line[1] in '.)')
                            for line in lines if line.strip()
                        ):
                            # It's likely a list
                            list_items = [line.strip().lstrip('•-*◦').strip() for line in lines if line.strip()]
                            blocks.append(DocumentBlock(
                                block_type=BlockType.LIST,
                                content=list_items,
                                metadata={"page": page_num + 1},
                                index=index
                            ))
                        else:
                            # Regular paragraph
                            blocks.append(DocumentBlock(
                                block_type=BlockType.PARAGRAPH,
                                content=para_text,
                                metadata={"page": page_num + 1},
                                index=index
                            ))
                        index += 1
        
        return blocks
