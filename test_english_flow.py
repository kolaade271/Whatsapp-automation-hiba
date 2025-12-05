#!/usr/bin/env python3
"""
Test English flow and global keywords
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

def test_english_flow():
    print("\n" + "="*60)
    print("🇬🇧 Testing English Support & Global Keywords")
    print("="*60)
    
    # Load env
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    db = Database(db_url)
    
    phone = "212688888888"
    
    # Clean up
    session = db.get_session()
    try:
        session.execute(text("DELETE FROM transactions WHERE phone_number = :phone"), {"phone": phone})
        session.execute(text("DELETE FROM users WHERE phone_number = :phone"), {"phone": phone})
        session.commit()
    finally:
        session.close()
    
    flow_handler = FlowHandler()
    flow_handler.db = db
    session_manager = SessionManager()
    user_session = session_manager.get_session(phone)
    
    print("\n1️⃣ Starting conversation...")
    flow_handler.process_message(user_session, "Hi")
    
    print("\n2️⃣ Selecting English (Option 3)...")
    response = flow_handler.process_message(user_session, "3")
    print(f"Bot: {response['text'][:50]}...")
    
    # Verify language in DB
    user = db.get_user(phone)
    if user and user['language'] == 'en':
        print("✅ Language set to English in DB")
    else:
        print("❌ Language update failed!")
        return

    print("\n3️⃣ Testing Global Cancel (sending 'stop')...")
    # User is in service menu, sending 'stop' should reset
    response = flow_handler.process_message(user_session, "stop")
    print(f"Bot: {response['text'][:50]}...")
    
    if "reset" in response['text'].lower() or "réinitialisée" in response['text'].lower():
        print("✅ Global 'stop' keyword worked!")
    else:
        print("❌ Global keyword failed!")

    print("\n4️⃣ Completing English Flow...")
    # Re-select English
    flow_handler.process_message(user_session, "3")
    # Select IAM
    flow_handler.process_message(user_session, "1")
    # Phone
    flow_handler.process_message(user_session, "0688888888")
    # Amount 50
    flow_handler.process_message(user_session, "6")
    # Offer Internet
    flow_handler.process_message(user_session, "5")
    
    print("\n5️⃣ Confirming in English...")
    response = flow_handler.process_message(user_session, "Confirm")
    print(f"Bot: {response['text']}")
    
    if "successful" in response['text'].lower():
        print("✅ English transaction successful!")
    else:
        print("❌ English transaction failed!")

    print("\n" + "="*60)
    print("✅ English Tests Completed!")
    print("="*60)

if __name__ == "__main__":
    test_english_flow()
