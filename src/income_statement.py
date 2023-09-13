import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import pandas as pd
import requests
import streamlit as st
# from dotenv import dotenv_values

from src.pydantic_models import IncomeStatementInsights
from src.utils import insights

# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

AV_API_KEY = st.secrets["av_api_key"]


def metrics(data):
    # Extracting values from the data
    grossProfit = float(data["grossProfit"])
    totalRevenue = float(data["totalRevenue"])
    operatingIncome = float(data["operatingIncome"])
    costOfRevenue = float(data["costOfRevenue"])
    costofGoodsAndServicesSold = float(data["costofGoodsAndServicesSold"])
    sellingGeneralAndAdministrative = float(data["sellingGeneralAndAdministrative"])
    ebit = float(data["ebit"])
    interestAndDebtExpense = float(data["interestAndDebtExpense"])

    # Calculating metrics
    gross_profit_margin = grossProfit / totalRevenue
    operating_profit_margin = operatingIncome / totalRevenue
    net_profit_margin = float(data["netIncome"]) / totalRevenue
    cost_efficiency = totalRevenue / (costOfRevenue + costofGoodsAndServicesSold)
    sg_and_a_efficiency = totalRevenue / sellingGeneralAndAdministrative
    interest_coverage_ratio = ebit / interestAndDebtExpense

    # Returning the results
    return {
        "gross_profit_margin": gross_profit_margin,
        "operating_profit_margin": operating_profit_margin,
        "net_profit_margin": net_profit_margin,
        "cost_efficiency": cost_efficiency,
        "sg_and_a_efficiency": sg_and_a_efficiency,
        "interest_coverage_ratio": interest_coverage_ratio
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
        inc_stat = data["annualReports"][0]
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

    met = metrics(inc_stat)
    ins = insights("income statement", inc_stat, IncomeStatementInsights)

    return met, ins


if __name__ == "__main__":
    met, ins = income_statement("TSLA")
    print("Metrics: ", met)
    print("Insights", ins)




    





