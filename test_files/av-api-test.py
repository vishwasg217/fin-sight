from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

import requests


url = "https://www.alphavantage.co/query"

symbol = "TSLA"
params = {
    "function": "CASH_FLOW",
    "symbol": symbol,
    "apikey": AV_API_KEY
}
response = requests.get(url, params=params)
data = response.json()
data = data["annualReports"][0]
print(data)


