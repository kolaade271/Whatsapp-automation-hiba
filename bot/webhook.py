from fastapi import APIRouter, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
import logging
import os
from typing import Optional
from dotenv import load_dotenv

from .session_manager import SessionManager
from .flow_handler import FlowHandler
from .whatsapp_client import WhatsAppClient

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize components
session_manager = SessionManager()
flow_handler = FlowHandler()
whatsapp_client = WhatsAppClient()

@router.get("/")
async def verify_webhook(
    hub_mode: Optional[str] = Query(None, alias="hub.mode"),
    hub_verify_token: Optional[str] = Query(None, alias="hub.verify_token"),
    hub_challenge: Optional[str] = Query(None, alias="hub.challenge")
):
    """
    Webhook verification endpoint for WhatsApp
    This is called by Meta/WhatsApp to verify your webhook
    """
    logger.info(f"Webhook verification request: mode={hub_mode}, token={hub_verify_token}")
    
    # Get verify token from environment
    VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
    
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return PlainTextResponse(content=hub_challenge)
    else:
        logger.warning("Webhook verification failed")
        raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/")
async def handle_webhook(request: Request):
    """
    Main webhook endpoint to receive messages from WhatsApp
    """
    try:
        body = await request.json()
        logger.info(f"Received webhook: {body}")
        
        # Extract message data from WhatsApp webhook payload
        if "entry" in body:
            for entry in body["entry"]:
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    
                    # Process incoming messages
                    if "messages" in value:
                        for message in value["messages"]:
                            await process_incoming_message(message, value)
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

async def process_incoming_message(message: dict, value: dict):
    """Process an incoming WhatsApp message"""
    try:
        # Extract message details
        phone_number = message.get("from")
        message_type = message.get("type")
        
        # Only process text messages for now
        if message_type != "text":
            logger.info(f"Ignoring non-text message type: {message_type}")
            return
        
        user_message = message.get("text", {}).get("body", "")
        message_id = message.get("id")
        
        logger.info(f"Processing message from {phone_number}: {user_message}")
        
        # Get user session
        session = session_manager.get_session(phone_number)
        
        # Process message through flow handler
        response = flow_handler.process_message(session, user_message)
        
        # Send response via WhatsApp
        await whatsapp_client.send_message(
            to=phone_number,
            message=response["text"]
        )
        
        # Mark message as read
        await whatsapp_client.mark_as_read(message_id)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
        # Send error message to user
        try:
            await whatsapp_client.send_message(
                to=phone_number,
                message="❌ Une erreur s'est produite. Veuillez réessayer.\nحدث خطأ. يرجى المحاولة مرة أخرى."
            )
        except:
            pass
