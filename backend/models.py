from sqlalchemy import Column, Integer
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    risk_score = Column(Integer)