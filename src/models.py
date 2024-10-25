from sqlalchemy import Column, Integer, String, ForeignKey, Integer, Boolean, DateTime
from src.database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    description = Column(String)
    stock = Column(Integer)
    expiration_date = Column(String)
