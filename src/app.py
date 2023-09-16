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
from src.news_sentiment import latest_news
from src.utils import round_numeric

ticker = st.text_input("Enter Ticker Symbol")

if "income_statement" not in st.session_state:
    st.session_state.income_statement = None

if "balance_sheet" not in st.session_state:
    st.session_state.balance_sheet = None

if "cash_flow" not in st.session_state:
    st.session_state.cash_flow = None

if "latest_news" not in st.session_state:
    st.session_state.latest_news = None

if st.button("Get Data"):
    with st.spinner("Generating income statement insights..."):
        st.session_state.income_statement = income_statement(ticker)
    
    with st.spinner("Generating balance sheet insights..."):
        st.session_state.balance_sheet = balance_sheet(ticker)
    
    with st.spinner("Generating cash flow insights..."):
        st.session_state.cash_flow = cash_flow(ticker)
    
    with st.spinner('Getting latest news...'):
        st.session_state.latest_news = latest_news(ticker, 10)


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
        st.write(st.session_state.income_statement["insights"].revenue_health)

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

