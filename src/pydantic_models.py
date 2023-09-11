from pydantic import BaseModel, Field

class IncomeStatementInsights(BaseModel):
    revenue_health: str = Field(..., description="Insight into the company's total revenue, providing a perspective on the health of the primary business activity.")
    operational_efficiency: str = Field(..., description="Analysis of the company's operating expenses in relation to its revenue, offering a view into the firm's operational efficiency.")
    r_and_d_focus: str = Field(..., description="Insight into the company's commitment to research and development, signifying its emphasis on innovation and future growth.")
    debt_management: str = Field(..., description="Analysis of the company's interest expenses, highlighting the scale of its debt obligations and its approach to leveraging.")
    profit_retention: str = Field(..., description="Insight into the company's net income, showcasing the amount retained post all expenses, which can be reinvested or distributed.")
