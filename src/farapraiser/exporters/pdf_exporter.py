"""PDF document exporter."""

from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib import colors
from farapraiser.parsers.base import DocumentBlock, BlockType
from farapraiser.exporters.base import DocumentExporter


class PDFExporter(DocumentExporter):
    """Exporter for PDF files using ReportLab."""
    
    def export(self, blocks: List[DocumentBlock], output_path: str) -> None:
        """Export blocks to PDF file."""
        doc = SimpleDocTemplate(output_path, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        styles = getSampleStyleSheet()
        
        for block in blocks:
            if block.block_type == BlockType.HEADING:
                level = self._get_heading_level(block)
                style = styles[f'Heading{level}'] if level <= 3 else styles['Heading3']
                para = Paragraph(block.content, style)
                story.append(para)
                story.append(Spacer(1, 0.2 * inch))
            
            elif block.block_type == BlockType.PARAGRAPH:
                para = Paragraph(block.content, styles['Normal'])
                story.append(para)
                story.append(Spacer(1, 0.1 * inch))
            
            elif block.block_type == BlockType.LIST:
                items = [ListItem(Paragraph(item, styles['Normal'])) for item in block.content]
                list_flow = ListFlowable(items, bulletType='bullet')
                story.append(list_flow)
                story.append(Spacer(1, 0.1 * inch))
            
            elif block.block_type == BlockType.TABLE:
                if block.content:
                    table = Table(block.content)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 14),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 0.2 * inch))
        
        doc.build(story)
    
    def _get_heading_level(self, block: DocumentBlock) -> int:
        """Extract heading level from metadata."""
        style = block.metadata.get("style", "") or block.metadata.get("level", "")
        if "Heading 1" in style or "heading1" in style.lower():
            return 1
        elif "Heading 2" in style or "heading2" in style.lower():
            return 2
        elif "Heading 3" in style or "heading3" in style.lower():
            return 3
        return 1
