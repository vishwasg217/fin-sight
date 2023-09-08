from dotenv import dotenv_values
import requests

config = dotenv_values(".env")

AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

import requests

# Define the API endpoint URL
url = "https://www.alphavantage.co/query"

# Define your Alpha Vantage API key (replace 'demo' with your actual API key)
api_key = "YOUR_API_KEY"

# Define the parameters for the request
params = {
    "function": "NEWS_SENTIMENT",
    "symbol": "IBM",
    "apikey": AV_API_KEY
}

# Send a GET request to the API
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Now you can work with the data
    print(data)
else:
    # If the request was not successful, print an error message
    print(f"Error: {response.status_code} - {response.text}")


