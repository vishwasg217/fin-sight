from dotenv import dotenv_values

config = dotenv_values(".env")

FMP_API_KEY = config["FMP_API_KEY"]

import requests

# Define the API endpoint URL
url = "https://financialmodelingprep.com/api/v4/financial-reports-json"

# Define your API key (replace YOUR_API_KEY with your actual API key)
api_key = "YOUR_API_KEY"

# Define the parameters for the request
params = {
    "symbol": "AAPL",
    "year": "2020",
    "period": "FY",
    "apikey": FMP_API_KEY
}

# Send a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")
