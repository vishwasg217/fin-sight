
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import requests
import streamlit as st
import os
# from dotenv import dotenv_values

from src.pydantic_models import CashFlowInsights
from src.utils import insights, get_total_revenue, get_total_debt, safe_float, generate_pydantic_model
from src.fields2 import cashflow, cashflow_attributes
# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

# AV_API_KEY = st.secrets["av_api_key"]
# OPENAI_API_KEY = st.secrets["openai_api_key"]


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def charts(data):
    dates = []
    operating_cash_flow = []
    cash_flow_from_investment = []
    cash_flow_from_financing = []

    for report in reversed(data["annualReports"]):
        dates.append(report["fiscalDateEnding"])
        operating_cash_flow.append(report["operatingCashflow"])
        cash_flow_from_investment.append(report["cashflowFromInvestment"])
        cash_flow_from_financing.append(report["cashflowFromFinancing"])

    return {
        "dates": dates,
        "operating_cash_flow": operating_cash_flow,
        "cash_flow_from_investment": cash_flow_from_investment,
        "cash_flow_from_financing": cash_flow_from_financing
    }
    

def metrics(data, total_revenue, total_debt):

    # Helper function to safely convert to float or set to N/A
    

    operatingCashFlow = safe_float(data.get("operatingCashflow"))
    capitalExpenditures = safe_float(data.get("capitalExpenditures"))
    dividendPayout = safe_float(data.get("dividendPayout"))
    netIncome = safe_float(data.get("netIncome"))

    operating_cash_flow_margin = "N/A" if "N/A" in (operatingCashFlow, total_revenue) else operatingCashFlow / total_revenue
    capital_expenditure_coverage_ratio = "N/A" if "N/A" in (operatingCashFlow, capitalExpenditures) else operatingCashFlow / capitalExpenditures
    free_cash_flow = "N/A" if "N/A" in (operatingCashFlow, capitalExpenditures) else operatingCashFlow - capitalExpenditures
    dividend_coverage_ratio = "N/A" if "N/A" in (dividendPayout, netIncome) else netIncome / dividendPayout
    cash_flow_to_debt_ratio = "N/A" if "N/A" in (operatingCashFlow, total_debt) else operatingCashFlow / total_debt

    return {
        "operating_cash_flow_margin": operating_cash_flow_margin,
        "capital_expenditure_coverage_ratio": capital_expenditure_coverage_ratio,
        "free_cash_flow": free_cash_flow,
        "dividend_coverage_ratio": dividend_coverage_ratio,
        "cash_flow_to_debt_ratio": cash_flow_to_debt_ratio
    }


def cash_flow(symbol, fields_to_include):
    AV_API_KEY = os.environ.get("AV_API_KEY")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "CASH_FLOW",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data:
        print(f"No data found for {symbol}")
        return None
    
    if "Information" in data:
            return {"Error": data["Information"]}

    if 'Error Message' in data:
        return {"Error": data['Error Message']}   
    
    chart_data = charts(data)

    report = data["annualReports"][0]
    total_revenue = get_total_revenue(symbol)
    total_debt = get_total_debt(symbol)
    met = metrics(report, total_revenue, total_debt)

    data_for_insights = {
        "annual_report_data": report,
        "historical_data": chart_data,
    }
    ins = {}
    for i, field in enumerate(cashflow_attributes):
        if fields_to_include[i]:
            response = insights(field, "cash flow", data_for_insights, str({field: cashflow[field]}))
            ins[field] = response


    return {
        "metrics": met,
        "chart_data": chart_data,
        "insights": ins
    }

if __name__ == "__main__":
    fields = [True, True, False, False, False]
    data = cash_flow("AAPL", fields)
    print("Metrics: ", data['metrics'])
    print("Chart Data: ", data['chart_data'])
    print("Insights", data['insights'])

# if __name__ == "__main__":
#     symbol = "AAPL"
#     url = "https://www.alphavantage.co/query"
#     params = {
#         "function": "CASH_FLOW",
#         "symbol": symbol,
#         "apikey": AV_API_KEY
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     if not data:
#         print(f"No data found for {symbol}")
    
#     ans = charts(data)
#     print(ans)