import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

from pydantic import BaseModel, Field, create_model
import requests
import streamlit as st


from src.utils import insights
from src.income_statement import charts, metrics


AV_API_KEY = st.secrets["av_api_key"]

# from src.income_statement import income_statement

def generate_model(fields_to_include, attributes, base_fields):
    attributes = ["revenue_health", "operational_efficiency", "r_and_d_focus", "debt_management", "profit_retention"]
    selected_fields = {attr: base_fields[attr] for attr, include in zip(attributes, fields_to_include) if include}
    
    return create_model("DynamicIncomeStatementInsights", **selected_fields)

def income_statement(symbol, fields_to_include):

    Model = generate_model(fields_to_include)

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
    ins = insights("income statement", data_for_insights, Model)

    return {
        "metrics": met,
        "chart_data": chart_data,
        "insights": ins
    }



min_length = 5

base_fields = {
    "revenue_health": (str, Field(..., description=f"Must be more than {min_length} words. Insight into the company's total revenue, providing a perspective on the health of the primary business activity.")),
    "operational_efficiency": (str, Field(..., description=f"Must be more than {min_length} words. Analysis of the company's operating expenses in relation to its revenue, offering a view into the firm's operational efficiency.")),
    "r_and_d_focus": (str, Field(..., description=f"Must be more than {min_length} words. Insight into the company's commitment to research and development, signifying its emphasis on innovation and future growth.")),
    "debt_management": (str, Field(..., description=f"Must be more than {min_length} words. Analysis of the company's interest expenses, highlighting the scale of its debt obligations and its approach to leveraging.")),
    "profit_retention": (str, Field(..., description=f"Must be more than {min_length} words. Insight into the company's net income, showcasing the amount retained post all expenses, which can be reinvested or distributed."))
}



# Example usage
fields_to_include = [True, False, False, False, True]

# instance = DynamicModel(revenue_health="good", r_and_d_focus="high", profit_retention="medium")
# print(instance)

response = income_statement("TSLA", fields_to_include)
print(response['insights'])

