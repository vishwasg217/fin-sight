import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import streamlit as st

st.set_page_config(page_title="FinSight", page_icon=":money_with_wings:")

st.title(":money_with_wings: FinSight \n\n **Financial Insights at Your Fingertip**")

st.info("""

**About the App and Its Features**:
Finsight is a cutting-edge AI assistant tailored for portfolio managers, investors, and finance enthusiasts. It streamlines the process of gaining crucial insights and summaries about a company in a user-friendly manner.

1. [**Finance Metrics Review**](https://finsight-report.streamlit.app/Finance_Metrics_Review): Simply enter the ticker symbol of your desired company. With a click, Finsight delves deep into the financial data and current news sentiment, presenting you with a comprehensive analysis. From metrics derived from income statements to the latest news sentiments, get a 360° view of the company's financial health.
 
2. [**Annual Report Analyzer**](https://finsight-report.streamlit.app/Annual_Report_Analyzer): Want a deep dive into a company's annual report? Upload the report in PDF format, and Finsight will process and analyze it, offering insights into Fiscal Year Highlights, Strategy Outlook and Future Direction, Risk Management, and Innovation & R&D. 

**GitHub Repository**:
For those keen on diving into the code or contributing, the entire project is open-source and hosted on GitHub. Find it [here](<GitHub link>).

**About the Creator**:
Hi! I'm Vishwas Gowda, an ML Engineer and an LLMs enthusiast.

Let's Connect and Collaborate:            
- [GitHub](https://github.com/vishwasg217)
- [Twitter](https://twitter.com/VishwasAiTech)
- [LinkedIn](https://www.linkedin.com/in/vishwasgowda217/)

""")