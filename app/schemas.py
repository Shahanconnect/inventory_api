from pydantic import BaseModel, confloat, conint
from typing import Optional
from datetime import datetime
from enum import Enum

class TransactionType(str, Enum):
    IN = "IN"
    OUT = "OUT"

# Product Schemas
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: confloat(gt=0)  # price > 0
    available_quantity: conint(ge=0)  # quantity >= 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# Stock Schemas
class StockTransactionBase(BaseModel):
    product_id: int
    quantity: conint(gt=0)  # positive number
    transaction_type: TransactionType

class StockTransactionCreate(StockTransactionBase):
    pass

class StockTransactionResponse(StockTransactionBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
