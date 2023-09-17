import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import streamlit as st

st.set_page_config(page_title="FinSight")

st.title(":money_with_wings: FinSight")
# st.info("""
# FinSight is a web app that helps you analyze and gain financial insights on a com
# """)

from src.income_statement import income_statement
from src.balance_sheet import balance_sheet
from src.cash_flow import cash_flow
from src.news_sentiment import top_news
from src.company_overview import company_overview
from src.utils import round_numeric
from src.pdf_gen import gen_pdf

ticker = st.text_input("Enter Ticker Symbol")

if "company_overview" not in st.session_state:
    st.session_state.company_overview = None

if "income_statement" not in st.session_state:
    st.session_state.income_statement = None

if "balance_sheet" not in st.session_state:
    st.session_state.balance_sheet = None

if "cash_flow" not in st.session_state:
    st.session_state.cash_flow = None

if "latest_news" not in st.session_state:
    st.session_state.latest_news = None

if "all_outputs" not in st.session_state:
    st.session_state.all_outputs = None

if st.button("Get Data"):

    with st.spinner("Getting company overview..."):
        st.session_state.company_overview = company_overview(ticker)

    with st.spinner("Generating income statement insights..."):
        st.session_state.income_statement = income_statement(ticker)
    
    with st.spinner("Generating balance sheet insights..."):
        st.session_state.balance_sheet = balance_sheet(ticker)
    
    with st.spinner("Generating cash flow insights..."):
        st.session_state.cash_flow = cash_flow(ticker)
    
    with st.spinner('Getting latest news...'):
        st.session_state.latest_news = top_news(ticker, 10)

    if st.session_state.company_overview and st.session_state.income_statement and st.session_state.balance_sheet and st.session_state.cash_flow and st.session_state.latest_news:
        st.session_state.all_outputs = True

if st.session_state.all_outputs:
    st.success("Insights successfully Generated!")
    if st.button("Generate PDF"):
        gen_pdf(st.session_state.company_overview["Name"], st.session_state.company_overview)
        st.success("PDF successfully generated!")
        with open("pdf/final_report.pdf", "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name="final_report.pdf",
                mime="application/pdf"
            )


    
if st.session_state.company_overview:
    with st.container():
        
        st.write("# Company Overview")
        # st.markdown("### Company Name:")
        st.markdown(f"""### {st.session_state.company_overview["Name"]}""")
        col1, col2, col3 = st.columns(3)
        col1.markdown("### Symbol:")
        col1.write(st.session_state.company_overview["Symbol"])
        col2.markdown("### Exchange:")
        col2.write(st.session_state.company_overview["Exchange"])
        col3.markdown("### Currency:")
        col3.write(st.session_state.company_overview["Currency"])

        col1, col2, col3 = st.columns(3)
        col1.markdown("### Sector:")
        col1.write(st.session_state.company_overview["Sector"])
        col2.markdown("### Industry:")
        col2.write(st.session_state.company_overview["Industry"])
        col3.write()
        st.markdown("### Description:")
        st.write(st.session_state.company_overview["Description"])
        
        col1, col2, col3 = st.columns(3)
        col1.markdown("### Country:")
        col1.write(st.session_state.company_overview["Country"])
        col2.markdown("### Address:")
        col2.write(st.session_state.company_overview["Address"])
        col3.write()

        col1, col2, col3 = st.columns(3)
        col1.markdown("### Fiscal Year End:")
        col1.write(st.session_state.company_overview["FiscalYearEnd"])
        col2.markdown("### Latest Quarter:")
        col2.write(st.session_state.company_overview["LatestQuarter"])
        market_cap_formatted = "${:,.2f}".format(float(st.session_state.company_overview["MarketCapitalization"]))
        col3.markdown("### Market Capitalization:")
        col3.write(market_cap_formatted)


tab1, tab2, tab3, tab4 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow", "News Sentiment"])


if st.session_state.income_statement:

    with tab1:
        
        st.write("# Income Statement")
        st.write("## Metrics")

        with st.container():

            col1, col2, col3 = st.columns(3)

            col1.metric("Gross Profit Margin", round_numeric(st.session_state.income_statement["metrics"]["gross_profit_margin"], 2))
            col2.metric("Operating Profit Margin", round_numeric(st.session_state.income_statement["metrics"]["operating_profit_margin"], 2))
            col3.metric("Net Profit Margin", round_numeric(st.session_state.income_statement["metrics"]["net_profit_margin"], 2))
            col1.metric("Cost Efficiency", round_numeric(st.session_state.income_statement["metrics"]["cost_efficiency"], 2))
            col2.metric("SG&A Efficiency", round_numeric(st.session_state.income_statement["metrics"]["sg_and_a_efficiency"], 2))
            col3.metric("Interest Coverage Ratio", round_numeric(st.session_state.income_statement["metrics"]["interest_coverage_ratio"], 2))
    
        
        st.write("## Insights")
        st.write("### Revenue Health")
        st.markdown(st.session_state.income_statement["insights"].revenue_health)

        st.write("### Operational Efficiency")
        st.write(st.session_state.income_statement["insights"].operational_efficiency)

        st.write("### R&D Focus")
        st.write(st.session_state.income_statement["insights"].r_and_d_focus)

        st.write("### Debt Management")
        st.write(st.session_state.income_statement["insights"].debt_management)

        st.write("### Profit Retention")
        st.write(st.session_state.income_statement["insights"].profit_retention)

if st.session_state.balance_sheet:
    with tab2:
        
        st.write("# Balance Sheet")
        st.write("## Metrics")

        with st.container():

            col1, col2, col3 = st.columns(3)

            col1.metric("Current Ratio", round_numeric(st.session_state.balance_sheet['metrics']['current_ratio'], 2))
            col2.metric("Debt to Equity Ratio", round_numeric(st.session_state.balance_sheet['metrics']['debt_to_equity_ratio'], 2))
            col3.metric("Quick Ratio", round_numeric(st.session_state.balance_sheet['metrics']['quick_ratio'], 2))
            col1.metric("Asset Turnover", round_numeric(st.session_state.balance_sheet['metrics']['asset_turnover'], 2))
            col2.metric("Equity Multiplier", round_numeric(st.session_state.balance_sheet['metrics']['equity_multiplier'], 2))



        st.write("## Insights")
        st.write("### Liquidity Position")
        st.write(st.session_state.balance_sheet['insights'].liquidity_position)

        st.write("### Operational Efficiency")
        st.write(st.session_state.balance_sheet['insights'].operational_efficiency)

        st.write("### Capital Structure")
        st.write(st.session_state.balance_sheet['insights'].capital_structure)

        st.write("### Inventory Management")
        st.write(st.session_state.balance_sheet['insights'].inventory_management)

        st.write("### Overall Solvency")
        st.write(st.session_state.balance_sheet['insights'].overall_solvency)

if st.session_state.cash_flow:
    with tab3:
            
        st.write("# Cash Flow")
        st.write("## Metrics")

        with st.container():

            col1, col2, col3 = st.columns(3)

            col1.metric("Operating Cash Flow Margin", round_numeric(st.session_state.cash_flow['metrics']['operating_cash_flow_margin'], 2))
            col2.metric("Capital Expenditure Coverage Ratio", round_numeric(st.session_state.cash_flow['metrics']['capital_expenditure_coverage_ratio'], 2))
            col3.metric("Dividend Coverage Ratio", round_numeric(st.session_state.cash_flow['metrics']['dividend_coverage_ratio'], 2))
            col1.metric("Cash Flow to Debt Ratio", round_numeric(st.session_state.cash_flow['metrics']['cash_flow_to_debt_ratio'], 2))
                    
            col2.metric("Free Cash Flow", "$ "+str("{:,}".format(round_numeric(st.session_state.cash_flow['metrics']['free_cash_flow']))))


        st.write("## Insights")
        st.write("### Operational Cash Efficiency")
        st.write(st.session_state.cash_flow['insights'].operational_cash_efficiency)

        st.write("### Investment Capability")
        st.write(st.session_state.cash_flow['insights'].investment_capability)

        st.write("### Financial Flexibility")
        st.write(st.session_state.cash_flow['insights'].financial_flexibility)

        st.write("### Dividend Sustainability")
        st.write(st.session_state.cash_flow['insights'].dividend_sustainability)

        st.write("### Debt Service Capability")
        st.write(st.session_state.cash_flow['insights'].debt_service_capability)

if st.session_state.latest_news:
    
    with tab4:
        st.markdown("## Latest News")
        column_config = {
                "title": st.column_config.Column(
                    "Title",
                    width="large",
                ),
                "url": st.column_config.LinkColumn(
                    "Link",
                    width="medium",
                ),
                "authors": st.column_config.ListColumn(
                    "Authors",
                    width = "medium"
                ),
                "topics": st.column_config.ListColumn(
                    "Topics",
                    width="large"
                ),
                "sentiment_score" : st.column_config.ProgressColumn(
                    "Sentiment Score",
                    min_value=-0.5,
                    max_value=0.5
                ),
                "sentiment_label": st.column_config.Column(
                "Sentiment Label" 
                )

            }

        st.metric("Mean Sentiment Score", 
                value=round_numeric(st.session_state.latest_news["mean_sentiment_score"]), 
                delta=st.session_state.latest_news["mean_sentiment_class"])
        
        st.dataframe(st.session_state.latest_news["news"], column_config=column_config)

