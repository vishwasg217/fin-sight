import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

from src.company_overview import company_overview

# Get the default styles
styles = getSampleStyleSheet()

# Define custom styles
centered_style = ParagraphStyle(
    'CenteredStyle',
    parent=styles['Heading1'],
    alignment=TA_CENTER,
    fontSize=48,
    spaceAfter=50,
)

sub_centered_style = ParagraphStyle(
    'SubCenteredStyle',
    parent=styles['Heading2'],
    alignment=TA_CENTER,
    fontSize=24,
    spaceAfter=15,
)

def cover_page(company_name):
    flowables = []
    
    # Title
    title = "FinSight"
    para_title = Paragraph(title, centered_style)
    flowables.append(para_title)
    
    # Subtitle
    subtitle = "Financial Insights for<br/>"
    para_subtitle = Paragraph(subtitle, sub_centered_style)
    flowables.append(para_subtitle)

    subtitle2 = "{} {}".format(company_name, "2022")
    para_subtitle2 = Paragraph(subtitle2, sub_centered_style)
    flowables.append(para_subtitle2)
    
    # Add a page break after the cover page
    flowables.append(PageBreak())
    
    return flowables

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

# Define custom styles
header_style = ParagraphStyle(
    'HeaderStyle',
    parent=styles['Heading2'],
    fontSize=24,
    spaceAfter=20,
)

data_style = ParagraphStyle(
    'DataStyle',
    parent=styles['Normal'],
    fontSize=14,
    spaceAfter=15,
    leading=20
)

company_name_style = ParagraphStyle(
    'DataStyle',
    parent=styles['Normal'],
    fontSize=20,
    spaceAfter=15,
    leading=20
)

def pdf_company_overview(data):
    flowables = []
    
    # Section Title
    title = "Company Overview"
    para_title = Paragraph(title, header_style)
    flowables.append(para_title)
    
    # Company Name
    # data = json.loads(data)
    company_name = data.get("Name")
    print(company_name)
    para_name = Paragraph("<b> {} </b>".format(company_name), company_name_style)
    flowables.append(para_name)
    
    # Other details
    details = [
        ("Symbol:", data.get("Symbol")),
        ("Exchange:", data.get("Exchange")),
        ("Currency:", data.get("Currency")),
        ("Sector:", data.get("Sector")),
        ("Industry:", data.get("Industry")),
        ("Description:", data.get("Description")),
        ("Country:", data.get("Country")),
        ("Address:", data.get("Address")),
        ("Fiscal Year End:", data.get("Fiscal_year_end")),
        ("Latest Quarter:", data.get("Latest_quarter")),
        ("Market Capitalization:", data.get("Market_cap"))
    ]
    
    for label, value in details:
        para_label = Paragraph("<b>{}</b> {}".format(label, value), data_style)
        flowables.append(para_label)
    
    return flowables



def gen_pdf(company_name, overview_data):
    doc = SimpleDocTemplate("pdf/final_report.pdf", pagesize=letter)
    all_flowables = []

    all_flowables.extend(cover_page(company_name))

    all_flowables.extend(pdf_company_overview(overview_data))
    doc.build(all_flowables)

if __name__ == "__main__":
    overview_data = company_overview("AAPL")
    gen_pdf("Apple Inc.", overview_data)

