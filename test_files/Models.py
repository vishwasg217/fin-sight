from typing import List
from pydantic import BaseModel
class IncomeStatementRequest(BaseModel):
    symbol: str
    fields_to_include: List[bool]