from sqlalchemy import Column, Integer, String
from db import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), unique=True, index=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
