#!/usr/bin/env python3
"""
Test restart functionality
"""

import sys
sys.path.insert(0, '/Users/adekola/Documents/Upwork/Hiba/whatsapp_bot')

from bot.session_manager import SessionManager
from bot.flow_handler import FlowHandler

def test_restart():
    print("\n" + "="*60)
    print("🧪 Testing Restart Functionality")
    print("="*60)
    
    session_manager = SessionManager()
    flow_handler = FlowHandler()
    
    phone = "212612345678"
    session = session_manager.get_session(phone)
    
    # Test 1: Start conversation
    print("\n1️⃣ Starting conversation...")
    response = flow_handler.process_message(session, "Hi")
    print(f"Bot: {response['text'][:50]}...")
    print(f"Step: {session.current_step}")
    
    # Test 2: Select French
    print("\n2️⃣ Selecting French...")
    response = flow_handler.process_message(session, "1")
    print(f"Bot: {response['text'][:50]}...")
    print(f"Step: {session.current_step}, Language: {session.language}")
    
    # Test 3: Select service
    print("\n3️⃣ Selecting IAM...")
    response = flow_handler.process_message(session, "1")
    print(f"Bot: {response['text'][:50]}...")
    print(f"Step: {session.current_step}")
    
    # Test 4: Type MENU to restart
    print("\n4️⃣ Typing 'menu' to restart...")
    response = flow_handler.process_message(session, "menu")
    print(f"Bot: {response['text']}")
    print(f"Step: {session.current_step}, Language: {session.language}")
    
    # Test 5: Try help
    print("\n5️⃣ Typing 'help'...")
    session.language = "fr"  # Set language for help
    response = flow_handler.process_message(session, "help")
    print(f"Bot: {response['text']}")
    
    # Test 6: Restart in Arabic
    print("\n6️⃣ Testing Arabic restart...")
    session.reset()
    response = flow_handler.process_message(session, "Hi")
    response = flow_handler.process_message(session, "2")  # Arabic
    print(f"Language: {session.language}")
    response = flow_handler.process_message(session, "القائمة")  # Menu in Arabic
    print(f"Bot: {response['text']}")
    print(f"Step: {session.current_step}")
    
    print("\n" + "="*60)
    print("✅ All restart tests completed!")
    print("="*60)

if __name__ == "__main__":
    test_restart()
