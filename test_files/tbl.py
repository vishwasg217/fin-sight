from pydantic import BaseModel
from typing import List

class MyPydanticModel(BaseModel):
    str_value: str
    bool_values: List[bool]

# Example usage:
data = {
    "str_value": "Hello, Pydantic!",
    "bool_values": [True, False, True, False, True]
}

my_model = MyPydanticModel(**data)
print(my_model)
