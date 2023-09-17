import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

# Sample DataFrame
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Los Angeles']
}
df = pd.DataFrame(data)

# Convert DataFrame to a list of lists (rows)
table_data = [df.columns.to_list()] + df.values.tolist()

def generate_pdf_with_table(filename, table_data):
    doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
    story = []

    # Create a Table with the data
    table = Table(table_data)
    table.hAlign = 'CENTER'
    table.rotate = 90

    # Add a TableStyle for better formatting
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)

    # Add the Table to the story
    story.append(table)

    # Build the PDF
    doc.build(story)

generate_pdf_with_table("table_report.pdf", table_data)
