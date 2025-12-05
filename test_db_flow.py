#!/usr/bin/env python3
"""
Test database integration and transaction flow
"""

import sys
import os
sys.path.insert(0, '/Users/adekola/Documents/Upwork/Hiba/whatsapp_bot')

from bot.session_manager import SessionManager
from bot.flow_handler import FlowHandler
from bot.database import Database
from sqlalchemy import text

def test_db_flow():
    print("\n" + "="*60)
    print("🧪 Testing Database Integration")
    print("="*60)
    
    # Initialize DB with test SQLite file
    test_db_url = "sqlite:///test_wafr.db"
    db = Database(test_db_url)
    
    # Clean up previous test user
    db_session = db.get_session()
    try:
        db_session.execute(text("DELETE FROM users WHERE phone_number = '212612345678'"))
        db_session.execute(text("DELETE FROM transactions WHERE phone_number = '212612345678'"))
        db_session.commit()
    except Exception as e:
        print(f"Cleanup error: {e}")
    finally:
        db_session.close()
    
    session_manager = SessionManager()
    # Mock the DB in flow handler to use our test DB
    flow_handler = FlowHandler()
    flow_handler.db = db
    
    phone = "212612345678"
    session = session_manager.get_session(phone)
    
    print("\n1️⃣ Starting conversation (User creation)...")
    flow_handler.process_message(session, "Hi")
    
    # Verify user created
    user = db.get_user(phone)
    print(f"✅ User created: {user['phone_number']}")
    print(f"💰 Initial Balance: {user['wallet_balance']} DH")
    
    print("\n2️⃣ Selecting French...")
    flow_handler.process_message(session, "1")
    
    # Verify language updated
    user = db.get_user(phone)
    print(f"✅ Language updated: {user['language']}")
    
    print("\n3️⃣ Completing flow to recharge...")
    flow_handler.process_message(session, "1") # IAM
    flow_handler.process_message(session, "0612345678") # Phone
    flow_handler.process_message(session, "6") # 50 DH
    flow_handler.process_message(session, "5") # Pass Internet
    
    print("\n4️⃣ Confirming transaction...")
    response = flow_handler.process_message(session, "Confirmer")
    print(f"Bot: {response['text']}")
    
    # Verify transaction and new balance
    user = db.get_user(phone)
    transactions = db.get_recent_transactions(phone)
    
    print(f"\n✅ New Balance: {user['wallet_balance']} DH")
    print(f"✅ Transactions found: {len(transactions)}")
    if transactions:
        txn = transactions[0]
        print(f"   - ID: {txn['id']}")
        print(f"   - Amount: {txn['amount']} DH")
        print(f"   - Status: {txn['status']}")
    
    # Test insufficient funds
    print("\n5️⃣ Testing insufficient funds...")
    # Drain wallet manually
    db_session = db.get_session()
    try:
        db_session.execute(text("UPDATE users SET wallet_balance = 10 WHERE phone_number = :phone"), {"phone": phone})
        db_session.commit()
    finally:
        db_session.close()
    
    session.reset()
    flow_handler.process_message(session, "Hi")
    flow_handler.process_message(session, "1")
    flow_handler.process_message(session, "1")
    flow_handler.process_message(session, "0612345678")
    flow_handler.process_message(session, "6") # 50 DH (Balance is 10)
    flow_handler.process_message(session, "5")
    
    response = flow_handler.process_message(session, "Confirmer")
    print(f"Bot: {response['text']}")
    
    print("\n" + "="*60)
    print("✅ Database tests completed!")
    print("="*60)
    
    # Cleanup
    os.remove("test_wafr.db")

if __name__ == "__main__":
    test_db_flow()
