import sys
from pathlib import Path
from faiss.swigfaiss import float_rand
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import requests
import streamlit as st
# from dotenv import dotenv_values

from src.pydantic_models import BalanceSheetInsights
from src.utils import insights, get_total_revenue, safe_float

# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

AV_API_KEY = st.secrets["av_api_key"]



def metrics(data, total_revenue):

    # Extracting values from the data
    totalCurrentAssets = safe_float(data.get("totalCurrentAssets"))
    totalCurrentLiabilities = safe_float(data.get("totalCurrentLiabilities"))
    totalLiabilities = safe_float(data.get("totalLiabilities"))
    totalShareholderEquity = safe_float(data.get("totalShareholderEquity"))
    totalAssets = safe_float(data.get("totalAssets"))
    inventory = safe_float(data.get("inventory"))

    # Calculate metrics, but check for N/A values in operands
    current_ratio = (
        "N/A"
        if "N/A" in (totalCurrentAssets, totalCurrentLiabilities)
        else totalCurrentAssets / totalCurrentLiabilities
    )
    debt_to_equity_ratio = (
        "N/A"
        if "N/A" in (totalLiabilities, totalShareholderEquity)
        else totalLiabilities / totalShareholderEquity
    )
    quick_ratio = (
        "N/A"
        if "N/A" in (totalCurrentAssets, totalCurrentLiabilities, inventory)
        else (totalCurrentAssets - inventory) / totalCurrentLiabilities
    )
    asset_turnover = (
        "N/A" if "N/A" in (total_revenue, totalAssets) else total_revenue / totalAssets
    )
    equity_multiplier = (
        "N/A"
        if "N/A" in (totalAssets, totalShareholderEquity)
        else totalAssets / totalShareholderEquity
    )

    # Returning the results
    return {
        "current_ratio": current_ratio,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "quick_ratio": quick_ratio,
        "asset_turnover": asset_turnover,
        "equity_multiplier": equity_multiplier,
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


