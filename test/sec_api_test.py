import requests
import pandas as pd
import json

# create request header
headers = {'User-Agent': "vishwas.g217@gmail.com"}

# get all companies data
companyTickers = requests.get(
    "https://www.sec.gov/files/company_tickers.json",
    headers=headers
    )

print(companyTickers.json())
# # review response / keys
print(companyTickers.json().keys())
# print(companyTickers.json().data())

# # format response to dictionary and get first key/value
firstEntry = companyTickers.json()['0']
print(firstEntry)

# # parse CIK // without leading zeros
directCik = companyTickers.json()['0']['cik_str']

# # dictionary to dataframe
companyData = pd.DataFrame.from_dict(companyTickers.json(),
                                     orient='index')
# print(companyData.head())

# # add leading zeros to CIK
companyData['cik_str'] = companyData['cik_str'].astype(
                           str).str.zfill(10)

cik = companyData['cik_str'][0]

filingMetadata = requests.get(
    f'https://data.sec.gov/submissions/CIK{cik}.json',
    headers=headers
    )

# print(filingMetadata.json().keys())
data = filingMetadata.json()['filings']['recent']

with open('data.json', 'w') as f:
    json.dump(data, f)