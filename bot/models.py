from sqlalchemy import Column, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    phone_number = Column(String(50), primary_key=True)
    language = Column(String(10), nullable=True)
    wallet_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.now)
    last_active = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relationship to transactions
    transactions = relationship("Transaction", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"
    
    transaction_id = Column(String(50), primary_key=True)
    phone_number = Column(String(50), ForeignKey("users.phone_number"))
    operator = Column(String(50))
    recipient_phone = Column(String(50))
    amount = Column(Float)
    offer = Column(String(100))
    status = Column(String(20), default="PENDING")
    timestamp = Column(DateTime, default=datetime.now)
    
    # Relationship to user
    user = relationship("User", back_populates="transactions")
