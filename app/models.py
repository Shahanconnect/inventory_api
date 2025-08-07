import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base

class TransactionType(str, enum.Enum):
    IN = "IN"
    OUT = "OUT"

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    available_quantity = Column(Integer, default=0)

    stock_transactions = relationship("StockTransaction", back_populates="product")

class StockTransaction(Base):
    __tablename__ = "stock_transactions"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product", back_populates="stock_transactions")
