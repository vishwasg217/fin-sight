from io import BytesIO
import json
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import landscape
from reportlab.platypus import Paragraph, Table, TableStyle, Spacer
from reportlab.lib import colors
import plotly.io as pio
from io import BytesIO
import tempfile


from src.company_overview import company_overview
from src.income_statement import income_statement
from src.balance_sheet import balance_sheet
from src.cash_flow import cash_flow
from src.news_sentiment import top_news
from src.utils import round_numeric, create_donut_chart, create_bar_chart

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

sub_header_style = ParagraphStyle(
    'DataStyle',
    parent=styles['Normal'],
    fontSize=20,
    spaceAfter=15,
    leading=20
)

def pdf_plotly_chart(fig):
    img_bytes = fig.to_image(format="png")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_file.write(img_bytes)
    temp_file.close()
    img = Image(temp_file.name, width=5*inch, height=3*inch)
    return img

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
    para_name = Paragraph("<b> {} </b>".format(company_name), sub_header_style)
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
        ("Fiscal Year End:", data.get("FiscalYearEnd")),
        ("Latest Quarter:", data.get("LatestQuarter")),
        ("Market Capitalization:", "$ "+str("{:,}".format(round_numeric(data.get("MarketCapitalization")))))
    ]
    
    for label, value in details:
        para_label = Paragraph("<b>{}</b> {}".format(label, value), data_style)
        flowables.append(para_label)
    
    return flowables


def pdf_income_statement(metrics, insights, chart_data):
    flowables = []
    
    # Section Title
    title = "INCOME STATEMENT"
    para_title = Paragraph(title, header_style)
    flowables.append(para_title)

    
    # Metrics
    flowables.append(Paragraph("<b>METRICS</b>", sub_header_style))
    for label, value in metrics.items():
        metric_text = "<b>{}</b>: {}".format(label.replace("_", " ").title(), round_numeric(value))
        flowables.append(Paragraph(metric_text, data_style))
    
    # Insights
    flowables.append(Paragraph("<b>INSIGHTS</b>", sub_header_style))
    

    try:
        flowables.append(Paragraph("Revenue Health", sub_section_header_style))
        flowables.append(Paragraph(insights.revenue_health, data_style))
        flowables.append(pdf_plotly_chart(create_bar_chart(chart_data, "total_revenue")))
    except:
        pass
    try:
        flowables.append(Paragraph("Operational Efficiency", sub_section_header_style))
        flowables.append(Paragraph(insights.operational_efficiency, data_style))
    except:
        pass
    try:
        flowables.append(Paragraph("R&D Focus", sub_section_header_style))
        flowables.append(Paragraph(insights.r_and_d_focus, data_style))
    except:
        pass
    try:
        flowables.append(Paragraph("Debt Management", sub_section_header_style))
        flowables.append(Paragraph(insights.debt_management, data_style))
        flowables.append(pdf_plotly_chart(create_bar_chart(chart_data, "interest_expense")))
    except:
        pass

    try:
        flowables.append(Paragraph("Profit Retention", sub_section_header_style))
        flowables.append(Paragraph(insights.profit_retention, data_style))
        flowables.append(pdf_plotly_chart(create_bar_chart(chart_data, "net_income")))
    except:
        pass

    return flowables

def pdf_balance_sheet(metrics, insights, chart_data):
    flowables = []
    
    # Section Title
    title = "BALANCE SHEET"
    para_title = Paragraph(title, header_style)
    flowables.append(para_title)

    # Metrics
    flowables.append(Paragraph("<b>METRICS</b>", sub_header_style))
    for label, value in metrics.items():
        metric_text = "<b>{}</b>: {}".format(label.replace("_", " ").title(), round_numeric(value))
        flowables.append(Paragraph(metric_text, data_style))
    
    # Insights
    flowables.append(Paragraph("<b>INSIGHTS</b>", sub_header_style))
    # insight_sections = [
    #     ("Liquidity Position", insights.liquidity_position),
    #     ("Operational Efficiency", insights.operational_efficiency),
    #     ("Capital Structure", insights.capital_structure),
    #     ("Inventory Management", insights.inventory_management),
    #     ("Overall Solvency", insights.overall_solvency)
    # ]
    
    # for section_title, insight_text in insight_sections:
    #     flowables.append(Paragraph(section_title, sub_section_header_style))
    #     flowables.append(Paragraph(insight_text, data_style))

    try:
        flowables.append(Paragraph("Liquidity Position", sub_section_header_style))
        flowables.append(Paragraph(insights.liquidity_position, data_style))
        flowables.append(pdf_plotly_chart(create_donut_chart(chart_data,"asset_composition")))
    except:
        pass
    try:
        flowables.append(Paragraph("Operational Efficiency", sub_section_header_style))
        flowables.append(Paragraph(insights.operational_efficiency, data_style))
    except:
        pass
    try:
        flowables.append(Paragraph("Capital Structure", sub_section_header_style))
        flowables.append(Paragraph(insights.capital_structure, data_style))
        flowables.append(pdf_plotly_chart(create_donut_chart(chart_data, "liabilities_composition")))

    except:
        pass

    try:
        flowables.append(Paragraph("Inventory Management", sub_section_header_style))
        flowables.append(Paragraph(insights.inventory_management, data_style))
    except:
        pass

    try:
        flowables.append(Paragraph("Overall Solvency", sub_section_header_style))
        flowables.append(Paragraph(insights.overall_solvency, data_style))
        flowables.append(pdf_plotly_chart(create_donut_chart(chart_data, "debt_structure")))
        
    except:
        pass

    return flowables

def pdf_cash_flow(metrics, insights, chart_data):
    flowables = []
    
    # Section Title
    title = "CASH FLOW"
    para_title = Paragraph(title, header_style)
    flowables.append(para_title)

    flowables.append(Paragraph("<b>METRICS</b>", sub_header_style))
    for label, value in metrics.items():
        metric_text = "<b>{}</b>: {}".format(label.replace("_", " ").title(), round_numeric(value))
        flowables.append(Paragraph(metric_text, data_style))

    # Insights
    flowables.append(Paragraph("<b>INSIGHTS</b>", sub_header_style))
    # insight_sections = [
    #     ("Operational Cash Efficiency", insights.operational_cash_efficiency),
    #     ("Investment Capability", insights.investment_capability),
    #     ("Financial Flexibility", insights.financial_flexibility),
    #     ("Dividend Sustainability", insights.dividend_sustainability),
    #     ("Debt Service Capability", insights.debt_service_capability)
    # ]
    
    # for section_title, insight_text in insight_sections:
    #     flowables.append(Paragraph(section_title, sub_section_header_style))
    #     flowables.append(Paragraph(insight_text, data_style))

    try:
        flowables.append(Paragraph("Operational Cash Efficiency", sub_section_header_style))
        flowables.append(Paragraph(insights.operational_cash_efficiency, data_style))
        flowables.append(pdf_plotly_chart(create_bar_chart(chart_data, "operating_cash_flow")))
    except:
        pass

    try:
        flowables.append(Paragraph("Investment Capability", sub_section_header_style))
        flowables.append(Paragraph(insights.investment_capability, data_style))
        flowables.append(pdf_plotly_chart(create_bar_chart(chart_data, "cash_flow_from_investment")))
    except:
        pass

    try:
        flowables.append(Paragraph("Financial Flexibility", sub_section_header_style))
        flowables.append(Paragraph(insights.financial_flexibility, data_style))
        flowables.append(pdf_plotly_chart(create_bar_chart(chart_data, "cash_flow_from_financing")))
    except:
        pass

    try:
        flowables.append(Paragraph("Dividend Sustainability", sub_section_header_style))
        flowables.append(Paragraph(insights.dividend_sustainability, data_style))
    except:
        pass

    try:
        flowables.append(Paragraph("Debt Service Capability", sub_section_header_style))
        flowables.append(Paragraph(insights.debt_service_capability, data_style))
    except:
        pass


    
    return flowables

def pdf_news_sentiment(data):
    flowables = []
    
    # Section Title
    title = "NEWS SENTIMENT"
    para_title = Paragraph(title, header_style)
    flowables.append(para_title)
    flowables.append(Spacer(1, 12))

    # News DataFrame to Table
    df = data['news']
    table_data = [df.columns.to_list()] + df.values.tolist()
    table = Table(table_data, repeatRows=1)  # repeatRows ensures the header is repeated if the table spans multiple pages

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




def gen_pdf(company_name, overview_data, income_statement_data, balance_sheet_data, cash_flow_data, news_data):
    doc = SimpleDocTemplate("pdf/final_report.pdf", pagesize=letter)
    all_flowables = []

    all_flowables.extend(cover_page(company_name))
    all_flowables.extend(pdf_company_overview(overview_data))
    all_flowables.extend(pdf_income_statement(income_statement_data['metrics'], income_statement_data['insights'], income_statement_data['chart_data']))
    # all_flowables.extend(pdf_balance_sheet(balance_sheet_data['metrics'], balance_sheet_data['insights'], balance_sheet_data['chart_data']))
    # all_flowables.extend(pdf_cash_flow(cash_flow_data['metrics'], cash_flow_data['insights'], cash_flow_data['chart_data']))
    # all_flowables.extend(pdf_news_sentiment(news_data))
    doc.build(all_flowables)

if __name__ == "__main__":
    overview_data = company_overview("AAPL")
    inc = income_statement("AAPL", [True, True, False, False, False])
    # bal = balance_sheet("AAPL", [True, False, True, False, True])
    # cash = cash_flow("AAPL", [True, True, True, False, False])
    # news = top_news("AAPL", 10)
    gen_pdf("Apple Inc.", overview_data, inc, None, None, None)
