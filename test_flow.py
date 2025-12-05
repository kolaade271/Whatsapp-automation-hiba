#!/usr/bin/env python3
"""
Test script to simulate WhatsApp conversation flow
This simulates the webhook messages that would come from WhatsApp
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"
TEST_PHONE = "212612345678"  # Test phone number

def simulate_incoming_message(phone: str, message_text: str):
    """Simulate an incoming WhatsApp message"""
    webhook_payload = {
        "entry": [
            {
                "changes": [
                    {
                        "value": {
                            "messages": [
                                {
                                    "from": phone,
                                    "id": f"msg_{datetime.now().timestamp()}",
                                    "type": "text",
                                    "text": {
                                        "body": message_text
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/webhook/", json=webhook_payload)
    print(f"\n{'='*60}")
    print(f"USER: {message_text}")
    print(f"Status: {response.status_code}")
    print(f"{'='*60}\n")
    return response

def test_french_flow():
    """Test the complete French conversation flow"""
    print("\n🇫🇷 TESTING FRENCH FLOW")
    print("="*60)
    
    # Step 1: Initial greeting
    simulate_incoming_message(TEST_PHONE, "Hi")
    
    # Step 2: Select French
    simulate_incoming_message(TEST_PHONE, "1")
    
    # Step 3: Select IAM recharge
    simulate_incoming_message(TEST_PHONE, "1")
    
    # Step 4: Enter phone number
    simulate_incoming_message(TEST_PHONE, "06 12 34 56 78")
    
    # Step 5: Select amount (50 DH)
    simulate_incoming_message(TEST_PHONE, "6")
    
    # Step 6: Select offer (Pass Internet)
    simulate_incoming_message(TEST_PHONE, "5")
    
    # Step 7: Confirm
    simulate_incoming_message(TEST_PHONE, "Confirmer")
    
    print("\n✅ French flow completed!")

def test_arabic_flow():
    """Test the complete Arabic conversation flow"""
    print("\n🇲🇦 TESTING ARABIC FLOW")
    print("="*60)
    
    # Reset by starting new conversation
    test_phone_ar = "212698765432"
    
    # Step 1: Initial greeting
    simulate_incoming_message(test_phone_ar, "Hello")
    
    # Step 2: Select Arabic
    simulate_incoming_message(test_phone_ar, "2")
    
    # Step 3: Select IAM recharge
    simulate_incoming_message(test_phone_ar, "10")
    
    # Step 4: Enter phone number
    simulate_incoming_message(test_phone_ar, "06 98 76 54 32")
    
    # Step 5: Select amount (100 DH)
    simulate_incoming_message(test_phone_ar, "7")
    
    # Step 6: Select offer (Pass Internet)
    simulate_incoming_message(test_phone_ar, "5")
    
    # Step 7: Cancel
    simulate_incoming_message(test_phone_ar, "إلغاء")
    
    print("\n✅ Arabic flow completed!")

def test_coming_soon():
    """Test coming soon services"""
    print("\n⏳ TESTING COMING SOON SERVICES")
    print("="*60)
    
    test_phone_cs = "212611111111"
    
    # Start conversation
    simulate_incoming_message(test_phone_cs, "Hi")
    
    # Select French
    simulate_incoming_message(test_phone_cs, "1")
    
    # Try unavailable service (Consulter mon solde)
    simulate_incoming_message(test_phone_cs, "4")
    
    print("\n✅ Coming soon test completed!")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 WafR WhatsApp Chatbot - Flow Test")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"\n✅ Server is running: {response.json()}")
    except:
        print("\n❌ Server is not running! Please start it first.")
        exit(1)
    
    # Run tests
    test_french_flow()
    input("\nPress Enter to test Arabic flow...")
    
    test_arabic_flow()
    input("\nPress Enter to test coming soon services...")
    
    test_coming_soon()
    
    # Check final status
    response = requests.get(f"{BASE_URL}/health")
    print(f"\n\n📊 Final Status: {response.json()}")
    
    print("\n" + "="*60)
    print("✅ All tests completed!")
    print("="*60)
