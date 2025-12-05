import httpx
import logging
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class WhatsAppClient:
    """Client for WhatsApp Business API"""
    
    def __init__(self):
        # Load credentials from environment variables
        self.access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")
        self.phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
        self.api_version = "v18.0"
        self.base_url = f"https://graph.facebook.com/{self.api_version}"
    
    async def send_message(self, to: str, message: str, preview_url: bool = False):
        """
        Send a text message via WhatsApp
        
        Args:
            to: Recipient phone number (with country code, no +)
            message: Message text
            preview_url: Whether to show URL preview
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "text",
            "text": {
                "preview_url": preview_url,
                "body": message
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logger.info(f"Message sent to {to}: {response.json()}")
                return response.json()
        
        except httpx.HTTPError as e:
            logger.error(f"Failed to send message: {e}")
            raise
    
    async def send_interactive_message(self, to: str, body: str, buttons: list):
        """
        Send an interactive message with buttons
        
        Args:
            to: Recipient phone number
            body: Message body text
            buttons: List of button dicts with 'id' and 'title'
        """
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # WhatsApp allows max 3 buttons
        buttons = buttons[:3]
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {
                    "text": body
                },
                "action": {
                    "buttons": [
                        {
                            "type": "reply",
                            "reply": {
                                "id": btn["id"],
                                "title": btn["title"]
                            }
                        }
                        for btn in buttons
                    ]
                }
            }
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logger.info(f"Interactive message sent to {to}")
                return response.json()
        
        except httpx.HTTPError as e:
            logger.error(f"Failed to send interactive message: {e}")
            raise
    
    async def mark_as_read(self, message_id: str):
        """Mark a message as read"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logger.info(f"Message {message_id} marked as read")
        
        except httpx.HTTPError as e:
            logger.error(f"Failed to mark message as read: {e}")
