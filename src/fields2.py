min_length = 40

inc_stat = {
    "revenue_health": f"Must be more than {min_length} words. Insight into the company's total revenue, providing a perspective on the health of the primary business activity.",
    "operational_efficiency": f"Must be more than {min_length} words. Analysis of the company's operating expenses in relation to its revenue, offering a view into the firm's operational efficiency.",
    "r_and_d_focus": f"Must be more than {min_length} words. Insight into the company's commitment to research and development, signifying its emphasis on innovation and future growth.",
    "debt_management": f"Must be more than {min_length} words. Analysis of the company's interest expenses, highlighting the scale of its debt obligations and its approach to leveraging.",
    "profit_retention": f"Must be more than {min_length} words. Insight into the company's net income, showcasing the amount retained post all expenses, which can be reinvested or distributed."
}

inc_stat_attributes = ["revenue_health", "operational_efficiency", "r_and_d_focus", "debt_management", "profit_retention"]

bal_sheet = {
    "liquidity_position": f"Must be more than {min_length} words. Insight into the company's ability to meet its short-term obligations using its short-term assets.",
    "assets_efficiency": f"Must be more than {min_length} words. Analysis of how efficiently the company is using its assets to generate sales.",
    "capital_structure": f"Must be more than {min_length} words. Insight into the company's financial leverage and its reliance on external liabilities versus internal equity.",
    "inventory_management": f"Must be more than {min_length} words. Analysis of the company's efficiency in managing, selling, and replacing its inventory.",
    "overall_solvency": f"Must be more than {min_length} words. Insight into the company's overall ability to meet its long-term debts and obligations."
}
balance_sheet_attributes = ["liquidity_position", "assets_efficiency", "capital_structure", "inventory_management", "overall_solvency"]


cashflow = {
    "operational_cash_efficiency": f"Must be more than {min_length} words. Insight into how efficiently the company is generating cash from its core operations.",
    "investment_capability": f"Must be more than {min_length} words. Indicates the company's ability to invest in its business using its operational cash flows.",
    "financial_flexibility": f"Must be more than {min_length} words. Demonstrates the cash left after all operational expenses and investments, which can be used for dividends, share buybacks, or further investments.",
    "dividend_sustainability": f"Must be more than {min_length} words. Indicates the company's ability to cover its dividend payouts with its net earnings.",
    "debt_service_capability": f"Must be more than {min_length} words. Analysis of the company's ability to service its debt using the operational cash flows."
}

cashflow_attributes = ["operational_cash_efficiency", "investment_capability", "financial_flexibility", "dividend_sustainability", "debt_service_capability"]

fiscal_year = {
    "performance_highlights": "Key performance and financial stats over the fiscal year.",
    "major_events": "Highlight of significant events, acquisitions, or strategic shifts that occurred during the year.",
    "challenges_encountered": "Challenges the company faced during the year and, if and how they managed or overcame them."
}

fiscal_year_attributes = ["performance_highlights", "major_events", "challenges_encountered"]

fiscal_year_questions={"performance_highlights": "What are the performance highlights?"
,"major_events":"Describe the major events and their impact ?" ,
"challenges_encountered": "What are the challenges encountered in this financial year ?"}

strat_outlook = {
    "strategic_initiatives": "The company's primary objectives and growth strategies for the upcoming years.",
    "market_outlook": "Insights into the broader market, competitive landscape, and industry trends the company anticipates.",
    "product_roadmap": "Upcoming launches, expansions, or innovations the company plans to roll out."
}

strat_outlook_attributes = ["strategic_initiatives", "market_outlook", "product_roadmap"]

strat_outlook_questions={"strategic_initiatives":"What are the Strategic initiatives being discussed for the fiscal year",
                         "market_outlook":"What is the market outlook for the fiscal year",
                         "product_roadmap":"Elaborate on the product roadmap for the fiscal year"}

risk_management = {
    "risk_factors": "Primary risks the company acknowledges.",
    "risk_mitigation": "Strategies for managing these risks."
}

risk_management_attributes = ["risk_factors", "risk_mitigation"]

risk_management_questions={"risk_factors":"What are the risk factors faced by the company ?",
                           "risk_mitigation":"What are the measures being taken to mitigate the risks ? "}

innovation = {
    "r_and_d_activities": "Overview of the company's focus on research and development, major achievements, or breakthroughs.",
    "innovation_focus": "Mention of new technologies, patents, or areas of research the company is diving into."
}

innovation_attributes = ["r_and_d_activities", "innovation_focus"]

innovation_questions={"r_and_d_activities":"Provide an overview on all the Research and Development activities,breakthroughs and acheievment",
                      "innovation_focus":" What are the new technologies,patents and areas of research the company is working on ?"}