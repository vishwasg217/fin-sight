import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors

from src.news_sentiment import top_news

styles = getSampleStyleSheet()


header_style = ParagraphStyle(
    'HeaderStyle',
    parent=styles['Heading2'],
    fontSize=24,
    spaceAfter=20,
    leading=30
)

sub_section_header_style = ParagraphStyle(
    'SubSectionHeaderStyle',
    parent=styles['Heading3'],
    fontSize=16,
    spaceAfter=8,
    leading=20
)

data_style = ParagraphStyle(
    'DataStyle',
    parent=styles['Normal'],
    fontSize=14,
    spaceAfter=15,
    leading=20
)

class RotatedTable(Flowable):
    def __init__(self, table_data):
        Flowable.__init__(self)
        self.table_data = table_data

    def wrap(self, availWidth, availHeight):
        # Swap width and height for rotated table
        self.width, self.height = availHeight, availWidth
        return self.width, self.height

    def draw(self):
        # Create the table
        table = Table(self.table_data, repeatRows=1)
        
        # Table Style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ])
        table.setStyle(style)

        # Rotate the canvas, draw the table, then reset rotation
        self.canv.saveState()
        self.canv.translate(0, self.width)
        self.canv.rotate(-90)
        table.wrapOn(self.canv, self.height, self.width)
        table.drawOn(self.canv, 0, 0)
        self.canv.restoreState()

def pdf_news_sentiment(data):
    flowables = []
    
    # Section Title
    title = "NEWS SENTIMENT"
    para_title = Paragraph(title, header_style)
    flowables.append(para_title)
    flowables.append(Spacer(1, 12))

    # News DataFrame to Table
    df = data['news'].astype(str)
    table_data = [df.columns.to_list()] + df.values.tolist()
    flowables.append(RotatedTable(table_data))
    flowables.append(Spacer(1, 12))
    
    table = Table(table_data, repeatRows=1)  # repeatRows ensures the header is repeated if the table spans multiple pages
    table.hAlign = 'CENTER'
    table.rotate = 90

    # Table Style
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    flowables.append(table)
    flowables.append(Spacer(1, 12))

    # Mean Sentiment Score
    mean_sentiment_score_text = f"Mean Sentiment Score: {data['mean_sentiment_score']:.2f}"
    flowables.append(Paragraph(mean_sentiment_score_text, data_style))
    flowables.append(Spacer(1, 12))

    # Mean Sentiment Class
    mean_sentiment_class_text = f"Mean Sentiment Class: {data['mean_sentiment_class']}"
    flowables.append(Paragraph(mean_sentiment_class_text, data_style))
    
    return flowables

news = top_news('AAPL', 10)

flow1 = pdf_news_sentiment(news)

doc = SimpleDocTemplate("table.pdf", pagesize=letter)
all_flowables = []
all_flowables.extend(flow1)
doc.build(all_flowables)


