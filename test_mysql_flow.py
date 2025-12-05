#!/usr/bin/env python3
"""
Test MySQL integration with full flow
"""

import sys
import os
import logging
from dotenv import load_dotenv
from sqlalchemy import text

sys.path.insert(0, '/Users/adekola/Documents/Upwork/Hiba/whatsapp_bot')

from bot.session_manager import SessionManager
from bot.flow_handler import FlowHandler
from bot.database import Database

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_mysql_flow():
    print("\n" + "="*60)
    print("🐬 Testing MySQL Integration")
    print("="*60)
    
    # Load env to get MySQL URL
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    print(f"🔌 Connecting to: {db_url}")
    
    if "mysql" not in db_url:
        print("⚠️ WARNING: Not using MySQL URL! Check your .env")
    
    # Initialize DB
    db = Database(db_url)
    
    # Test phone number
    phone = "212699999999"
    
    # Clean up previous test data for this phone
    print("\n🧹 Cleaning up test data...")
    session = db.get_session()
    try:
        session.execute(text("DELETE FROM transactions WHERE phone_number = :phone"), {"phone": phone})
        session.execute(text("DELETE FROM users WHERE phone_number = :phone"), {"phone": phone})
        session.commit()
    except Exception as e:
        print(f"Cleanup error: {e}")
    finally:
        session.close()
    
    # Initialize Flow Handler
    flow_handler = FlowHandler()
    # Force it to use our DB instance (though it should create its own with same env)
    flow_handler.db = db
    
    session_manager = SessionManager()
    user_session = session_manager.get_session(phone)
    
    print("\n1️⃣ Starting conversation (User creation)...")
    flow_handler.process_message(user_session, "Hi")
    
    # Verify user created in MySQL
    user = db.get_user(phone)
    if user:
        print(f"✅ User created in MySQL: {user['phone_number']}")
        print(f"💰 Initial Balance: {user['wallet_balance']} DH")
    else:
        print("❌ User NOT found in MySQL!")
        return

    print("\n2️⃣ Completing flow to recharge (Arabic)...")
    # Select Arabic
    flow_handler.process_message(user_session, "2")
    # Select IAM (Input 1, was 10)
    flow_handler.process_message(user_session, "1")
    # Enter Phone
    flow_handler.process_message(user_session, "0699999999")
    # Select 50 DH
    flow_handler.process_message(user_session, "6")
    # Select Pass Internet
    flow_handler.process_message(user_session, "5")
    
    print("\n3️⃣ Confirming transaction...")
    response = flow_handler.process_message(user_session, "Confirmer")
    print(f"Bot: {response['text']}")
    
    # Verify transaction in MySQL
    transactions = db.get_recent_transactions(phone)
    user = db.get_user(phone)
    
    print(f"\n✅ New Balance: {user['wallet_balance']} DH")
    print(f"✅ Transactions found: {len(transactions)}")
    if transactions:
        txn = transactions[0]
        print(f"   - ID: {txn['id']}")
        print(f"   - Amount: {txn['amount']} DH")
        print(f"   - Status: {txn['status']}")
        print("   - Stored in MySQL! 🐬")
    else:
        print("❌ No transactions found in MySQL!")

    print("\n" + "="*60)
    print("✅ MySQL Integration Test Completed!")
    print("="*60)

if __name__ == "__main__":
    test_mysql_flow()
