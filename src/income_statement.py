import sys
from pathlib import Path
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

from src.pydantic_models import IncomeStatementInsights
from src.utils import format_json_to_multiline_string

config = dotenv_values(".env")
OPENAI_API_KEY = config["OPENAI_API_KEY"]
AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

def insights(income_statement):
    parser = PydanticOutputParser(pydantic_object=IncomeStatementInsights)

    template = """
    You are tasked with generating insights about the company from the income statement below:

    ----
    {inputs}
    ----

    Generate insights about the company according to the following format:
    ----
    {output_format}
    ----
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["inputs"],
        partial_variables={"output_format": parser.get_format_instructions()}
    )

    model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, max_tokens=2000)

    income_statement = format_json_to_multiline_string(income_statement)

    formatted_input = prompt.format(inputs=income_statement)
    print("-"*30)
    print("Formatted Input:")
    print(formatted_input)
    print("-"*30)

    response = model.predict(formatted_input)
    print(response)
    parsed_output = parser.parse(response)
    return parsed_output

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
        income_statement = data["annualReports"][0]
        df = pd.DataFrame([income_statement])
        print(df)
    else:
        print(f"Error: {response.status_code} - {response.text}")

    met = metrics(income_statement)
    ins = insights(income_statement)

    return met, ins


if __name__ == "__main__":
    met, ins = income_statement("MSFT")
    print("Metrics: ", met)
    print("Insights", ins)




    





