import requests
import streamlit as st
import os
# from dotenv import dotenv_values

from src.pydantic_models import BalanceSheetInsights
from src.utils import insights, get_total_revenue, safe_float, generate_pydantic_model
from src.fields2 import bal_sheet, balance_sheet_attributes

# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

# AV_API_KEY = st.secrets["av_api_key"]
# OPENAI_API_KEY = st.secrets["openai_api_key"]

import logging
from logger_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def charts(data):
    report = data['annualReports'][0]
    asset_composition = {"total_current_assets": report['totalCurrentAssets'],
        "total_non_current_assets": report['totalNonCurrentAssets']              
    }

    liabilities_composition = {
        "total_current_liabilities": report['totalCurrentLiabilities'],
        "total_non_current_liabilities": report['totalNonCurrentLiabilities']
    }

    debt_structure = {
        "short_term_debt": report['shortTermDebt'],
        "long_term_debt": report['longTermDebt']
    }

    return {
        "asset_composition": asset_composition,
        "liabilities_composition": liabilities_composition,
        "debt_structure": debt_structure
    }

         

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


def balance_sheet(symbol, fields_to_include):
    AV_API_KEY = os.environ.get("AV_API_KEY")
    logger.info(f"AV API Key: {AV_API_KEY}")
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data:
            print(f"No data found for {symbol}")
            return None
    
    if "Error Message" in data:
        return {"Error": data["Error Message"]}
    
    chart_data = charts(data)

    report = data["annualReports"][0]
    total_revenue = get_total_revenue(symbol)
    met = metrics(report, total_revenue)

    data_for_insights = {
        "annual_report_data": report,
        "historical_data": chart_data,
    }

    ins = {}
    for i, field in enumerate(balance_sheet_attributes):
        if fields_to_include[i]:
            response = insights(field, "balance sheet", data_for_insights, str({field: bal_sheet[field]}))
            ins[field] = response

    return {
        "metrics": met,
        "chart_data": chart_data,
        "insights": ins
    }

if __name__ == "__main__":
    fields = [True, True, False, False, False]
    data = balance_sheet("MSFT", fields)
    print("Metrics: ", data['metrics'])
    print("Chart Data: ", data['chart_data'])
    print("Insights", data['insights'])


