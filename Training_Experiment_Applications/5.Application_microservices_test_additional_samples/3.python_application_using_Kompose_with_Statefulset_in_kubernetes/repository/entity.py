# This file defines data class for inventory items

from sqlalchemy import Column, Integer, String, Float
from database import Base

"""
Json for inventory item
{
  "sku": "IB123456789",
  "name": "Tropicana Apple Juice"
  "label": "juice"
  "price": 25.00,
  "quantity": 50
}
"""

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    sku = Column(String(20), unique=True)
    name = Column(String(100))
    label = Column(String(50))
    price = Column(Float)
    quantity = Column(Integer)

    def __init__(self, sku=None, name=None, label=None, price=0.0, quantity=0):
        self.sku = sku
        self.name = name
        self.label = label
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f'<Inventory {self.name!r}>'
