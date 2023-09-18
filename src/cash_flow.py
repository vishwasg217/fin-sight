
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import requests
import streamlit as st
# from dotenv import dotenv_values

from src.pydantic_models import CashFlowInsights
from src.utils import insights, get_total_revenue, get_total_debt, safe_float

# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

AV_API_KEY = st.secrets["av_api_key"]

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


def cash_flow(symbol):
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
    data = data["annualReports"][0]

    total_revenue = get_total_revenue(symbol)
    total_debt = get_total_debt(symbol)

    met = metrics(data, total_revenue, total_debt)
    ins = insights("balance sheet", data, CashFlowInsights)

    return {
        "metrics": met,
        "insights": ins
    }

if __name__ == "__main__":
    met, ins = cash_flow("TSLA")
    print("Metrics: ", met)
    print("Insights: ", ins)