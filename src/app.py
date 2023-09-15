import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import streamlit as st

st.set_page_config(page_title="FinSight")

st.title(":money_with_wings: FinSight")
st.info("""
FinSight is a web app that helps you analyze and gain financial insights on a com
""")

from src.income_statement import income_statement
from src.balance_sheet import balance_sheet
from src.cash_flow import cash_flow
from src.utils import round_numeric

ticker = st.text_input("Enter Ticker Symbol")

if "output" not in st.session_state:
    st.session_state.output = None

if st.button("Get Data"):
    with st.spinner("Generating income statement insights..."):
        income_statement_metrics, income_statement_insights = income_statement(ticker)
    
    with st.spinner("Generating balance sheet insights..."):
        balance_sheet_metrics, balance_sheet_insights = balance_sheet(ticker)
    
    with st.spinner("Generating cash flow insights..."):
        cash_flow_metrics, cash_flow_insights = cash_flow(ticker)

    st.session_state.output = {
        "income_statement_metrics": income_statement_metrics,
        "income_statement_insights": income_statement_insights,
        "balance_sheet_metrics": balance_sheet_metrics,
        "balance_sheet_insights": balance_sheet_insights,
        "cash_flow_metrics": cash_flow_metrics,
        "cash_flow_insights": cash_flow_insights
    }

if st.session_state.output:

    tab1, tab2, tab3 = st.tabs(["Income Statement", "Balance Sheet", "Cash Flow"])

    with tab1:
        
        st.write("# Income Statement")
        st.write("## Metrics")

        with st.container():

            col1, col2, col3 = st.columns(3)

            col1.metric("Gross Profit Margin", round_numeric(st.session_state.output["income_statement_metrics"]["gross_profit_margin"]))
            col2.metric("Operating Profit Margin", round_numeric(st.session_state.output["income_statement_metrics"]["operating_profit_margin"]))
            col3.metric("Net Profit Margin", round_numeric(st.session_state.output["income_statement_metrics"]["net_profit_margin"]))
            col1.metric("Cost Efficiency", round_numeric(st.session_state.output["income_statement_metrics"]["cost_efficiency"]))
            col2.metric("SG&A Efficiency", round_numeric(st.session_state.output["income_statement_metrics"]["sg_and_a_efficiency"]))
            col3.metric("Interest Coverage Ratio", round_numeric(st.session_state.output["income_statement_metrics"]["interest_coverage_ratio"]))


        st.write("## Insights")
        st.write("### Revenue Health")
        st.write(st.session_state.output["income_statement_insights"].revenue_health)

        st.write("### Operational Efficiency")
        st.write(st.session_state.output["income_statement_insights"].operational_efficiency)

        st.write("### R&D Focus")
        st.write(st.session_state.output["income_statement_insights"].r_and_d_focus)

        st.write("### Debt Management")
        st.write(st.session_state.output["income_statement_insights"].debt_management)

        st.write("### Profit Retention")
        st.write(st.session_state.output["income_statement_insights"].profit_retention)


    with tab2:
        
        st.write("# Balance Sheet")
        st.write("## Metrics")

        with st.container():

            col1, col2, col3 = st.columns(3)

            col1.metric("Current Ratio", round_numeric(st.session_state.output["balance_sheet_metrics"]["current_ratio"], 2))
            col2.metric("Debt to Equity Ratio", round_numeric(st.session_state.output["balance_sheet_metrics"]["debt_to_equity_ratio"], 2))
            col3.metric("Quick Ratio", round_numeric(st.session_state.output["balance_sheet_metrics"]["quick_ratio"], 2))
            col1.metric("Asset Turnover", round_numeric(st.session_state.output["balance_sheet_metrics"]["asset_turnover"], 2))
            col2.metric("Equity Multiplier", round_numeric(st.session_state.output["balance_sheet_metrics"]["equity_multiplier"], 2))

        st.write("## Insights")
        st.write("### Liquidity Position")
        st.write(st.session_state.output["balance_sheet_insights"].liquidity_position)

        st.write("### Operational Efficiency")
        st.write(st.session_state.output["balance_sheet_insights"].operational_efficiency)

        st.write("### Capital Structure")
        st.write(st.session_state.output["balance_sheet_insights"].capital_structure)

        st.write("### Inventory Management")
        st.write(st.session_state.output["balance_sheet_insights"].inventory_management)

        st.write("### Overall Solvency")
        st.write(st.session_state.output["balance_sheet_insights"].overall_solvency)


    with tab3:
            
        st.write("# Cash Flow")
        st.write("## Metrics")

        with st.container():

            col1, col2, col3 = st.columns(3)

            col1.metric("Operating Cash Flow Margin", round_numeric(st.session_state.output["cash_flow_metrics"]["operating_cash_flow_margin"], 2))
            col2.metric("Capital Expenditure Coverage Ratio", round_numeric(st.session_state.output["cash_flow_metrics"]["capital_expenditure_coverage_ratio"], 2))
            col3.metric("Dividend Coverage Ratio", round_numeric(st.session_state.output["cash_flow_metrics"]["dividend_coverage_ratio"], 2))
            col1.metric("Cash Flow to Debt Ratio", round_numeric(st.session_state.output["cash_flow_metrics"]["cash_flow_to_debt_ratio"], 2))         
            col2.metric("Free Cash Flow", "$ "+str("{:,}".format(round_numeric(st.session_state.output["cash_flow_metrics"]["free_cash_flow"]))))


        st.write("## Insights")
        st.write("### Operational Cash Efficiency")
        st.write(st.session_state.output["cash_flow_insights"].operational_cash_efficiency)

        st.write("### Investment Capability")
        st.write(st.session_state.output["cash_flow_insights"].investment_capability)

        st.write("### Financial Flexibility")
        st.write(st.session_state.output["cash_flow_insights"].financial_flexibility)

        st.write("### Dividend Sustainability")
        st.write(st.session_state.output["cash_flow_insights"].dividend_sustainability)

        st.write("### Debt Service Capability")
        st.write(st.session_state.output["cash_flow_insights"].debt_service_capability)



