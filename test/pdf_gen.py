import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from src.company_overview import company_overview

def generate_introductory_section(filename, data):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title = Paragraph(f"<b>{data['Name']}</b> ({data['Symbol']})", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Description
    description = Paragraph(data['Description'], styles['Normal'])
    story.append(description)
    story.append(Spacer(1, 12))

    # Other details
    details = [
        f"Asset Type: {data['AssetType']}",
        f"CIK: {data['CIK']}",
        f"Exchange: {data['Exchange']}",
        f"Currency: {data['Currency']}",
        f"Country: {data['Country']}",
        f"Sector: {data['Sector']}",
        f"Industry: {data['Industry']}",
        f"Address: {data['Address']}",
        f"Fiscal Year End: {data['FiscalYearEnd']}",
        f"Latest Quarter: {data['LatestQuarter']}",
        f"Market Capitalization: {data['MarketCapitalization']}"
    ]

    for detail in details:
        story.append(Paragraph(detail, styles['Normal']))
        story.append(Spacer(1, 6))

    doc.build(story)

if __name__ == "__main__":
    ticker = "AAPL"
    data = company_overview(ticker)
    generate_introductory_section("pdf/introductory_section.pdf", data)
