import pandas as pd


def get_companies():
    df=pd.read_csv('data/ticker_symbol/symbols.csv')
    company_options = [f"{row['Name']}" for index, row in df.iterrows()]
    return company_options

def get_ticker(selected_company):
    df=pd.read_csv('data/ticker_symbol/symbols.csv')   
    # selected_company_name = selected_company.split(" (")[0]
    if selected_company:
       for index, row in df.iterrows():
             if row['Name'] == selected_company:
                ticker = row['Code']
                return ticker
             
    return {
        "Error":"Company not found"
    }
