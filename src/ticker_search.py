import pandas as pd


def get_companies():
    df=pd.read_csv('data/ticker_symbol/symbols.csv')
    company_options = [f"{row['Name']} ({row['Code']})" for index, row in df.iterrows()]
    return company_options
