import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import csv
import requests
import streamlit as st

API_TOKEN = st.secrets["eod_api_key"]

def get_ticker_symbol(company_name):
    with open("data/ticker_symbols/ticker_symbols.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == company_name:
                return row['Code']
    return None

# Example usage:
# if __name__ == "__main__":  # Replace with the path to your CSV file
#     company_name = "Apple Inc"
#     ticker = get_ticker_symbol(company_name)
#     if ticker:
#         print(f"The ticker symbol for {company_name} is {ticker}.")
#     else:
#         print(f"No ticker symbol found for {company_name}.")

def get_all_company_names():
    company_names = []
    with open("data/ticker_symbols/ticker_symbols.csv", 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Type'] == "Common Stock":
                company_names.append(row['Name'])
    return tuple(company_names)

# Example usage:
if __name__ == "__main__":
    companies = get_all_company_names()
    print(companies)



def get_symbols_for_exchange(exchange_code, api_token):
    base_url = "https://eodhd.com/api/exchange-symbol-list/"
    url = f"{base_url}{exchange_code}/"
    params = {
        "api_token": api_token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Received unexpected response:")
            print(response.text)
            print(type(response))
            print(type(response.text))
            print(len(response.text))
            with open("data/ticker_symbols/ticker_symbols.txt", "w") as f:
                f.write(response.text)
            with open("data/ticker_symbols/ticker_symbols.csv", "w") as f:
                f.write(response.text)
            return None
    else:
        response.raise_for_status()

if __name__ == "__main__":
    EXCHANGE_CODE = ['NYSE', 'NASDAQ']  # Replace with your desired exchange code

    try:
        data = get_symbols_for_exchange(EXCHANGE_CODE, API_TOKEN)
        print(data)
    except requests.RequestException as e:
        print(f"Error occurred: {e}")
