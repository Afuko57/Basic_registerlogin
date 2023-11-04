from pydantic import BaseModel
from decimal import Decimal
from datetime import date

class Product(BaseModel):
    id: int
    product_name: str
    price: Decimal
    quantity: int
    date_added: date
    date_modified: date
    product_code: str
