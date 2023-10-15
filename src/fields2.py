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
    "operational_efficiency": f"Must be more than {min_length} words. Analysis of how efficiently the company is using its assets to generate sales.",
    "capital_structure": f"Must be more than {min_length} words. Insight into the company's financial leverage and its reliance on external liabilities versus internal equity.",
    "inventory_management": f"Must be more than {min_length} words. Analysis of the company's efficiency in managing, selling, and replacing its inventory.",
    "overall_solvency": f"Must be more than {min_length} words. Insight into the company's overall ability to meet its long-term debts and obligations."
}
balance_sheet_attributes = ["liquidity_position", "operational_efficiency", "capital_structure", "inventory_management", "overall_solvency"]


cash_flow = {
    "operational_cash_efficiency": f"Must be more than {min_length} words. Insight into how efficiently the company is generating cash from its core operations.",
    "investment_capability": f"Must be more than {min_length} words. Indicates the company's ability to invest in its business using its operational cash flows.",
    "financial_flexibility": f"Must be more than {min_length} words. Demonstrates the cash left after all operational expenses and investments, which can be used for dividends, share buybacks, or further investments.",
    "dividend_sustainability": f"Must be more than {min_length} words. Indicates the company's ability to cover its dividend payouts with its net earnings.",
    "debt_service_capability": f"Must be more than {min_length} words. Analysis of the company's ability to service its debt using the operational cash flows."
}

cashflow_attributes = ["operational_cash_efficiency", "investment_capability", "financial_flexibility", "dividend_sustainability", "debt_service_capability"]