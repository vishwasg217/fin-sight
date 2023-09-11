import sys
from pathlib import Path
from faiss.swigfaiss import float_rand
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

import streamlit as st
import pandas as pd
import requests
from dotenv import dotenv_values

from src.pydantic_models import BalanceSheetInsights
from src.utils import format_json_to_multiline_string, insights

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]
AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

def get_total_revenue(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return float(data["annualReports"][0]["totalRevenue"])


def metrics(data, total_revenue):
    totalCurrentAssets = float(data["totalCurrentAssets"])
    totalCurrentLiabilities = float(data["totalCurrentLiabilities"])
    totalLiabilities = float(data["totalLiabilities"])
    totalShareholderEquity = float(data["totalShareholderEquity"])
    totalAssets = float(data["totalAssets"])
    inventory = float(data["inventory"])


    current_ratio = totalCurrentAssets / totalCurrentLiabilities
    debt_to_equity_ratio = totalLiabilities / totalShareholderEquity
    quick_ratio = (totalCurrentAssets - inventory) / totalCurrentLiabilities
    # Assuming you pass total revenue as an additional parameter to this function

    asset_turnover = total_revenue / totalAssets
    equity_multiplier = totalAssets / totalShareholderEquity

    return {
        "current_ratio": current_ratio,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "quick_ratio": quick_ratio,
        "asset_turnover": asset_turnover,
        "equity_multiplier": equity_multiplier
    }

def balance_sheet(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    data = data["annualReports"][0]

    total_revenue = get_total_revenue(symbol)

    met = metrics(data, total_revenue)
    ins = insights("balance sheet", data, BalanceSheetInsights)

    return met, ins

if __name__ == "__main__":
    met, ins = balance_sheet("MSFT")
    print("Metrics: ", met)
    print("Insights: ", ins)


