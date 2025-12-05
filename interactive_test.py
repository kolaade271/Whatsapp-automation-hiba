#!/usr/bin/env python3
"""
Simple interactive test for the WhatsApp chatbot
"""

import sys
sys.path.insert(0, '/Users/adekola/Documents/Upwork/Hiba/whatsapp_bot')

from bot.session_manager import SessionManager
from bot.flow_handler import FlowHandler

def main():
    print("\n" + "="*60)
    print("🤖 WafR WhatsApp Chatbot - Interactive Test")
    print("="*60)
    print("\nThis simulates the conversation flow without WhatsApp API")
    print("Type 'quit' to exit\n")
    
    session_manager = SessionManager()
    flow_handler = FlowHandler()
    
    # Test phone number
    phone = "212612345678"
    session = session_manager.get_session(phone)
    
    print("Bot: Starting conversation...")
    
    while True:
        # Get user input
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if not user_input:
            continue
        
        # Process message
        response = flow_handler.process_message(session, user_input)
        
        # Display bot response
        print(f"\n{'='*60}")
        print("Bot:")
        print(response['text'])
        print(f"{'='*60}")
        
        # Show current session state
        print(f"\n[Session State: {session.current_step}]")
        if session.language:
            print(f"[Language: {session.language}]")
        if session.data:
            print(f"[Data: {session.data}]")

if __name__ == "__main__":
    main()
