from pydantic import BaseModel

class IncomeStatementInsights(BaseModel):
    gross_profit_margin: float
    operating_profit_margin: float
    net_profit_margin: float
    cost_efficiency: float
    sg_and_a_efficiency: float
    interest_coverage_ratio: float
    declining_revenue: bool
    high_debt_obligation: bool
    dividend_payout_ratio: float
