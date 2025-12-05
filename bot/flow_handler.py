from typing import Dict, List, Optional
import logging
from .session_manager import UserSession
from .messages import Messages
from .database import Database
import uuid

logger = logging.getLogger(__name__)

class FlowHandler:
    """Handles the conversation flow logic"""
    
    def __init__(self):
        self.messages = Messages()
        self.db = Database()
    
    def process_message(self, session: UserSession, user_message: str) -> Dict:
        """
        Process user message and return appropriate response
        
        Returns:
            Dict with 'text' and optional 'buttons' for interactive messages
        """
        user_message = user_message.strip()
        current_step = session.current_step
        
        # Ensure user exists in DB
        self.db.create_user(session.phone_number)
        
        logger.info(f"Processing step: {current_step}, message: {user_message}")
        
        message_lower = user_message.lower()
        
        # Check for help keywords (works at any step)
        help_keywords = ["help", "aide", "مساعدة", "?", "؟"]
        
        if any(keyword in message_lower for keyword in help_keywords):
            lang = session.language if session.language else "fr"
            return {
                "text": self.messages.get_help_message(lang)
            }
        
        # Check for restart/cancel keywords (works at any step)
        restart_keywords = [
            # English
            "restart", "reset", "menu", "start over", "cancel", "stop", "back", "home",
            # French
            "recommencer", "retour", "annuler", "accueil",
            # Arabic
            "إعادة", "القائمة", "إلغاء", "رجوع", "قف", "البداية"
        ]
        
        if any(keyword in message_lower for keyword in restart_keywords):
            lang = session.language if session.language else None
            session.reset()
            session.current_step = "language_selection"
            
            # Send appropriate restart message
            if lang:
                restart_msg = self.messages.get_restart_message(lang)
                welcome_msg = self.messages.get_welcome_message()
                return {
                    "text": f"{restart_msg}\n\n{welcome_msg}"
                }
            else:
                return {
                    "text": self.messages.get_welcome_message()
                }
        
        # Route to appropriate handler based on current step
        if current_step == "welcome":
            return self._handle_welcome(session, user_message)
        
        elif current_step == "language_selection":
            return self._handle_language_selection(session, user_message)
        
        elif current_step == "service_menu":
            return self._handle_service_menu(session, user_message)
        
        elif current_step == "phone_number":
            return self._handle_phone_number(session, user_message)
        
        elif current_step == "amount_selection":
            return self._handle_amount_selection(session, user_message)
        
        elif current_step == "offer_selection":
            return self._handle_offer_selection(session, user_message)
        
        elif current_step == "confirmation":
            return self._handle_confirmation(session, user_message)
        
        else:
            # Unknown step, reset to welcome
            session.reset()
            return self._handle_welcome(session, user_message)
    
    def _handle_welcome(self, session: UserSession, message: str) -> Dict:
        """Handle initial greeting"""
        session.current_step = "language_selection"
        return {
            "text": self.messages.get_welcome_message()
        }
    
    def _handle_language_selection(self, session: UserSession, message: str) -> Dict:
        """Handle language selection"""
        if message == "1":
            session.language = "fr"
            self.db.update_user_language(session.phone_number, "fr")
            session.current_step = "service_menu"
            return {
                "text": self.messages.get_service_menu("fr")
            }
        elif message == "2":
            session.language = "ar"
            self.db.update_user_language(session.phone_number, "ar")
            session.current_step = "service_menu"
            return {
                "text": self.messages.get_service_menu("ar")
            }
        elif message == "3":
            session.language = "en"
            self.db.update_user_language(session.phone_number, "en")
            session.current_step = "service_menu"
            return {
                "text": self.messages.get_service_menu("en")
            }
        else:
            return {
                "text": self.messages.get_welcome_message()
            }
    
    def _handle_service_menu(self, session: UserSession, message: str) -> Dict:
        """Handle service selection"""
        lang = session.language
        
        # Map French and Arabic options
        # Map options (same for both languages now)
        service_map = {"1": "IAM", "2": "INWI", "3": "ORANGE"}
        unavailable = ["4", "5", "6", "7", "8", "9"]
        
        if message in unavailable:
            return {
                "text": self.messages.get_coming_soon_message(lang)
            }
        
        if message in service_map:
            session.data["operator"] = service_map[message]
            session.current_step = "phone_number"
            return {
                "text": self.messages.get_phone_number_prompt(lang)
            }
        
        # Invalid selection
        return {
            "text": self.messages.get_service_menu(lang)
        }
    
    def _handle_phone_number(self, session: UserSession, message: str) -> Dict:
        """Handle phone number input"""
        lang = session.language
        
        # Basic validation (you can enhance this)
        cleaned = message.replace(" ", "").replace("-", "")
        if len(cleaned) >= 9 and cleaned.isdigit():
            session.data["phone"] = message
            session.current_step = "amount_selection"
            return {
                "text": self.messages.get_amount_menu(lang)
            }
        else:
            return {
                "text": self.messages.get_invalid_phone_message(lang)
            }
    
    def _handle_amount_selection(self, session: UserSession, message: str) -> Dict:
        """Handle amount selection"""
        lang = session.language
        
        amount_map = {
            "1": "5", "2": "10", "3": "20",
            "4": "25", "5": "30", "6": "50",
            "7": "100", "8": "200", "9": "300"
        }
        
        if message in amount_map:
            session.data["amount"] = amount_map[message]
            session.current_step = "offer_selection"
            return {
                "text": self.messages.get_offer_menu(lang)
            }
        
        return {
            "text": self.messages.get_amount_menu(lang)
        }
    
    def _handle_offer_selection(self, session: UserSession, message: str) -> Dict:
        """Handle offer selection"""
        lang = session.language
        
        offer_map = {
            "1": "Recharge Multiple" if lang == "fr" else "تعبئة متعددة",
            "2": "Pass SMS" if lang == "fr" else "باس الرسائل",
            "3": "Pass Jawal" if lang == "fr" else "باس جوال",
            "4": "Pass National" if lang == "fr" else "باس وطني",
            "5": "Pass Internet" if lang == "fr" else "باس الإنترنت",
            "6": "Pass International" if lang == "fr" else "باس دولي",
            "7": "Pass Tout En Un" if lang == "fr" else "باس الكل في واحد",
            "8": "Pass Réseaux Sociaux" if lang == "fr" else "باس الشبكات الاجتماعية",
            "9": "Pass Tiktok et Youtube" if lang == "fr" else "باس تيك توك ويوتيوب",
            "10": "Pass Roaming" if lang == "fr" else "باس التجوال",
            "11": "Roaming Data" if lang == "fr" else "بيانات التجوال",
            "12": "Service Premium" if lang == "fr" else "خدمة بريميوم"
        }
        
        if message in offer_map:
            session.data["offer"] = offer_map[message]
            session.current_step = "confirmation"
            return {
                "text": self.messages.get_confirmation_message(
                    lang,
                    session.data["operator"],
                    session.data["phone"],
                    session.data["amount"],
                    session.data["offer"]
                )
            }
        
        return {
            "text": self.messages.get_offer_menu(lang)
        }
    
    def _handle_confirmation(self, session: UserSession, message: str) -> Dict:
        """Handle confirmation or cancellation"""
        lang = session.language
        message_lower = message.lower()
        
        # Check for confirmation
        confirm_keywords = ["confirmer", "confirm", "تأكيد", "1", "yes", "oui"]
        cancel_keywords = ["annuler", "cancel", "إلغاء", "2", "no", "non"]
        
        if any(keyword in message_lower for keyword in confirm_keywords):
            # Process the recharge
            result = self._process_recharge(session)
            session.reset()  # Reset for new transaction
            
            if result.get("success"):
                return {
                    "text": self.messages.get_success_message(lang)
                }
            else:
                return {
                    "text": self.messages.get_insufficient_balance_message(lang)
                }
        
        elif any(keyword in message_lower for keyword in cancel_keywords):
            session.reset()
            return {
                "text": self.messages.get_cancelled_message(lang)
            }
        
        # Invalid response, show confirmation again
        return {
            "text": self.messages.get_confirmation_message(
                lang,
                session.data["operator"],
                session.data["phone"],
                session.data["amount"],
                session.data["offer"]
            )
        }
    
    def _process_recharge(self, session: UserSession) -> Dict:
        """
        Process the actual recharge using database
        """
        logger.info(f"Processing recharge: {session.data}")
        
        # Generate transaction ID
        txn_id = f"TXN{uuid.uuid4().hex[:8].upper()}"
        
        transaction_data = {
            "transaction_id": txn_id,
            "user_phone": session.phone_number,
            "operator": session.data["operator"],
            "recipient_phone": session.data["phone"],
            "amount": float(session.data["amount"]),
            "offer": session.data["offer"]
        }
        
        # Process transaction in DB
        success = self.db.create_transaction(transaction_data)
        
        if success:
            return {
                "success": True,
                "transaction_id": txn_id
            }
        else:
            # Handle failure (e.g. insufficient funds)
            # For now we'll just log it, but in production you'd want to notify user
            logger.error(f"Transaction failed for {session.phone_number}")
            return {
                "success": False,
                "error": "insufficient_funds"
            }
