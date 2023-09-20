import json
import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
# from dotenv import dotenv_values

from src.pydantic_models import IncomeStatementInsights
from src.utils import insights, safe_float

# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

AV_API_KEY = st.secrets["av_api_key"]

def charts(data):
    dates = []
    total_revenue = []
    net_income = []
    interest_expense = []

    for report in reversed(data["annualReports"]):
        dates.append(report["fiscalDateEnding"])
        total_revenue.append(report["totalRevenue"])
        net_income.append(report["netIncome"])
        interest_expense.append(report["interestAndDebtExpense"])

    return {
        "dates": dates,
        "total_revenue": total_revenue,
        "net_income": net_income,
        "interest_expense": interest_expense
    }




def metrics(data):

    # Extracting values from the data
    grossProfit = safe_float(data.get("grossProfit"))
    totalRevenue = safe_float(data.get("totalRevenue"))
    operatingIncome = safe_float(data.get("operatingIncome"))
    costOfRevenue = safe_float(data.get("costOfRevenue"))
    costofGoodsAndServicesSold = safe_float(data.get("costofGoodsAndServicesSold"))
    sellingGeneralAndAdministrative = safe_float(data.get("sellingGeneralAndAdministrative"))
    ebit = safe_float(data.get("ebit"))
    interestAndDebtExpense = safe_float(data.get("interestAndDebtExpense"))
    netIncome = safe_float(data["netIncome"])

    # Calculate metrics, but check for N/A values in operands
    gross_profit_margin = (
        "N/A" if "N/A" in (grossProfit, totalRevenue) else grossProfit / totalRevenue
    )
    operating_profit_margin = (
        "N/A" if "N/A" in (operatingIncome, totalRevenue) else operatingIncome / totalRevenue
    )
    net_profit_margin = (
        "N/A" if "N/A" in (netIncome, totalRevenue) else netIncome / totalRevenue
    )
    cost_efficiency = (
        "N/A"
        if "N/A" in (totalRevenue, costOfRevenue, costofGoodsAndServicesSold)
        else totalRevenue / (costOfRevenue + costofGoodsAndServicesSold)
    )
    sg_and_a_efficiency = (
        "N/A"
        if "N/A" in (totalRevenue, sellingGeneralAndAdministrative)
        else totalRevenue / sellingGeneralAndAdministrative
    )
    interest_coverage_ratio = (
        "N/A" if "N/A" in (ebit, interestAndDebtExpense) else ebit / interestAndDebtExpense
    )

    # Returning the results
    return {
        "gross_profit_margin": gross_profit_margin,
        "operating_profit_margin": operating_profit_margin,
        "net_profit_margin": net_profit_margin,
        "cost_efficiency": cost_efficiency,
        "sg_and_a_efficiency": sg_and_a_efficiency,
        "interest_coverage_ratio": interest_coverage_ratio,
    }



def income_statement(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "INCOME_STATEMENT",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }

    # Send a GET request to the API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if not data:
            print(f"No data found for {symbol}")
            return None
        
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

    chart_data = charts(data)

    report = data["annualReports"][0]
    met = metrics(report)

    data_for_insights = {
        "annual_report_data": report,
        "historical_data": chart_data,
    }
    ins = insights("income statement", data_for_insights, IncomeStatementInsights)

    return {
        "metrics": met,
        "chart_data": chart_data,
        "insights": ins
    }


if __name__ == "__main__":
    data = income_statement("TSLA")
    print("Metrics: ", data['metrics'])
    print("Chart Data: ", data['chart_data'])
    print("Insights", data['insights'])




    





