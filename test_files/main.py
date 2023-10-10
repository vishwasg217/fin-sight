import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from test_files.Models import IncomeStatementRequest
from src.income_statement import income_statement

app = FastAPI()
@app.post("/income_statement")
def get_income_statement(request_data: IncomeStatementRequest):
    symbol = request_data.symbol
    fields_to_include = request_data.fields_to_include

    # Call the income_statement function to retrieve data
    income_statement_data = income_statement(symbol, fields_to_include)

    return income_statement_data  # Return the data as a response

if __name__ == "main":
    uvicorn.run(app, host="0.0.0.0", port=8000)