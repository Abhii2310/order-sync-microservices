from sqlalchemy import Column, Integer, String
from db import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String(50), index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="CREATED")
