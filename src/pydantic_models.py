from pydantic import BaseModel, Field

class IncomeStatementInsights(BaseModel):
    revenue_health: str = Field(..., description="Insight into the company's total revenue, providing a perspective on the health of the primary business activity.")
    operational_efficiency: str = Field(..., description="Analysis of the company's operating expenses in relation to its revenue, offering a view into the firm's operational efficiency.")
    r_and_d_focus: str = Field(..., description="Insight into the company's commitment to research and development, signifying its emphasis on innovation and future growth.")
    debt_management: str = Field(..., description="Analysis of the company's interest expenses, highlighting the scale of its debt obligations and its approach to leveraging.")
    profit_retention: str = Field(..., description="Insight into the company's net income, showcasing the amount retained post all expenses, which can be reinvested or distributed.")

class BalanceSheetInsights(BaseModel):
    liquidity_position: str = Field(..., description="Insight into the company's ability to meet its short-term obligations using its short-term assets.")
    operational_efficiency: str = Field(..., description="Analysis of how efficiently the company is using its assets to generate sales.")
    capital_structure: str = Field(..., description="Insight into the company's financial leverage and its reliance on external liabilities versus internal equity.")
    inventory_management: str = Field(..., description="Analysis of the company's efficiency in managing, selling, and replacing its inventory.")
    overall_solvency: str = Field(..., description="Insight into the company's overall ability to meet its long-term debts and obligations.")

class CashFlowInsights(BaseModel):
    operational_cash_efficiency: str = Field(..., description="Insight into how efficiently the company is generating cash from its core operations.")
    investment_capability: str = Field(..., description="Indicates the company's ability to invest in its business using its operational cash flows.")
    financial_flexibility: str = Field(..., description="Demonstrates the cash left after all operational expenses and investments, which can be used for dividends, share buybacks, or further investments.")
    dividend_sustainability: str = Field(..., description="Indicates the company's ability to cover its dividend payouts with its net earnings.")
    debt_service_capability: str = Field(..., description="Analysis of the company's ability to service its debt using the operational cash flows.")
