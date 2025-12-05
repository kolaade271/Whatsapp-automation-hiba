import os
import logging
from typing import Dict, Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

from .models import Base, User, Transaction

logger = logging.getLogger(__name__)

class Database:
    """
    Database manager using SQLAlchemy
    Supports MySQL, PostgreSQL, and SQLite
    """
    
    def __init__(self, db_url: str = None):
        # Get DB URL from env or use default SQLite
        self.db_url = db_url or os.getenv("DATABASE_URL", "sqlite:///wafr_bot.db")
        
        # Configure engine
        if self.db_url.startswith("sqlite"):
            self.engine = create_engine(self.db_url, connect_args={"check_same_thread": False})
        else:
            # MySQL/PostgreSQL pool configuration
            self.engine = create_engine(self.db_url, pool_pre_ping=True, pool_recycle=3600)
            
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        logger.info(f"Database connected: {self.db_url.split('://')[0]}")

    def get_session(self) -> Session:
        """Get a new database session"""
        return self.SessionLocal()

    def get_user(self, phone_number: str) -> Optional[Dict]:
        """Get user details"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.phone_number == phone_number).first()
            if user:
                return {
                    "phone_number": user.phone_number,
                    "language": user.language,
                    "wallet_balance": user.wallet_balance,
                    "created_at": user.created_at,
                    "last_active": user.last_active
                }
            return None
        except Exception as e:
            logger.error(f"Error getting user {phone_number}: {e}")
            return None
        finally:
            session.close()

    def create_user(self, phone_number: str, language: str = None) -> bool:
        """Create a new user with initial bonus balance"""
        session = self.get_session()
        try:
            # Check if user exists
            existing_user = session.query(User).filter(User.phone_number == phone_number).first()
            if existing_user:
                return False
            
            # Create new user
            new_user = User(
                phone_number=phone_number,
                language=language,
                wallet_balance=1000.0  # Welcome bonus
            )
            session.add(new_user)
            session.commit()
            logger.info(f"Created new user {phone_number}")
            return True
        except Exception as e:
            logger.error(f"Error creating user {phone_number}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def update_user_language(self, phone_number: str, language: str):
        """Update user's preferred language"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.phone_number == phone_number).first()
            if user:
                user.language = language
                session.commit()
        except Exception as e:
            logger.error(f"Error updating language for {phone_number}: {e}")
            session.rollback()
        finally:
            session.close()

    def create_transaction(self, data: Dict) -> bool:
        """Record a new transaction and deduct balance"""
        session = self.get_session()
        try:
            # 1. Get user and check balance
            user = session.query(User).filter(User.phone_number == data['user_phone']).first()
            
            if not user or user.wallet_balance < float(data['amount']):
                logger.warning(f"Insufficient balance for {data['user_phone']}")
                return False
            
            # 2. Deduct balance
            user.wallet_balance -= float(data['amount'])
            
            # 3. Create transaction record
            txn = Transaction(
                transaction_id=data['transaction_id'],
                phone_number=data['user_phone'],
                operator=data['operator'],
                recipient_phone=data['recipient_phone'],
                amount=float(data['amount']),
                offer=data['offer'],
                status='SUCCESS'
            )
            
            session.add(txn)
            session.commit()
            logger.info(f"Transaction {data['transaction_id']} successful")
            return True
            
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def get_recent_transactions(self, phone_number: str, limit: int = 5) -> List[Dict]:
        """Get user's recent transactions"""
        session = self.get_session()
        try:
            txns = session.query(Transaction)\
                .filter(Transaction.phone_number == phone_number)\
                .order_by(Transaction.timestamp.desc())\
                .limit(limit)\
                .all()
            
            return [{
                "id": t.transaction_id,
                "operator": t.operator,
                "recipient": t.recipient_phone,
                "amount": t.amount,
                "offer": t.offer,
                "status": t.status,
                "date": t.timestamp
            } for t in txns]
        except Exception as e:
            logger.error(f"Error getting transactions for {phone_number}: {e}")
            return []
        finally:
            session.close()
