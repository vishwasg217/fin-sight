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


def balance_sheet_metrics(data):
    current_ratio = data["totalCurrentAssets"] / data["totalCurrentLiabilities"]
    debt_to_equity_ratio = data["totalLiabilities"] / data["totalShareholderEquity"]
    quick_ratio = (data["totalCurrentAssets"] - data["inventory"]) / data["totalCurrentLiabilities"]
    # Assuming you pass total revenue as an additional parameter to this function
    # asset_turnover = total_revenue / data["totalAssets"]
    equity_multiplier = data["totalAssets"] / data["totalShareholderEquity"]

    return {
        "current_ratio": current_ratio,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "quick_ratio": quick_ratio,
        # "asset_turnover": asset_turnover,
        "equity_multiplier": equity_multiplier
    }


