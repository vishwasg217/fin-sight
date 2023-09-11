
import sys
from pathlib import Path
from faiss.swigfaiss import float_rand
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import requests
from dotenv import dotenv_values

from src.pydantic_models import BalanceSheetInsights
from src.utils import insights, get_total_revenue, get_total_debt

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]
AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

def metrics(data, total_revenue, total_debt):

    operatingCashFlow = float(data["operatingCashflow"])
    capitalExpenditures = float(data["capitalExpenditures"])
    dividendPayout = float(data["dividendPayout"])
    netIncome = float(data["netIncome"])

    operating_cash_flow_margin = operatingCashFlow / total_revenue
    capital_expenditure_coverage_ratio = operatingCashFlow / capitalExpenditures
    free_cash_flow = operatingCashFlow - capitalExpenditures
    dividend_coverage_ratio = netIncome / dividendPayout
    cash_flow_to_debt_ratio = operatingCashFlow / total_debt

    return {
        "operating_cash_flow_margin": operating_cash_flow_margin,
        "capital_expenditure_coverage_ratio": capital_expenditure_coverage_ratio,
        "free_cash_flow": free_cash_flow,
        "dividend_coverage_ratio": dividend_coverage_ratio,
        "cash_flow_to_debt_ratio": cash_flow_to_debt_ratio
    }

def cashflow(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "CASH_FLOW",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    data = data["annualReports"][0]

    total_revenue = get_total_revenue(symbol)
    total_debt = get_total_debt(symbol)

    met = metrics(data, total_revenue, total_debt)
    ins = insights("balance sheet", data, BalanceSheetInsights)

    return met, ins

if __name__ == "__main__":
    met, ins = cashflow("MSFT")
    print("Metrics: ", met)
    print("Insights: ", ins)