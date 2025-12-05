from typing import Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class UserSession:
    """Represents a user's conversation session"""
    
    def __init__(self, phone_number: str):
        self.phone_number = phone_number
        self.language = None  # 'fr' or 'ar'
        self.current_step = "welcome"
        self.data = {}
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
    
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if session has expired"""
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)
    
    def reset(self):
        """Reset session to initial state"""
        self.language = None
        self.current_step = "welcome"
        self.data = {}
        self.update_activity()


class SessionManager:
    """Manages user sessions for the chatbot"""
    
    def __init__(self):
        self.sessions: Dict[str, UserSession] = {}
    
    def get_session(self, phone_number: str) -> UserSession:
        """Get or create a session for a user"""
        # Clean expired sessions periodically
        self._clean_expired_sessions()
        
        if phone_number not in self.sessions:
            logger.info(f"Creating new session for {phone_number}")
            self.sessions[phone_number] = UserSession(phone_number)
        else:
            self.sessions[phone_number].update_activity()
        
        return self.sessions[phone_number]
    
    def _clean_expired_sessions(self):
        """Remove expired sessions"""
        expired = [
            phone for phone, session in self.sessions.items()
            if session.is_expired()
        ]
        for phone in expired:
            logger.info(f"Removing expired session for {phone}")
            del self.sessions[phone]
    
    def reset_session(self, phone_number: str):
        """Reset a user's session"""
        if phone_number in self.sessions:
            self.sessions[phone_number].reset()
            logger.info(f"Reset session for {phone_number}")
