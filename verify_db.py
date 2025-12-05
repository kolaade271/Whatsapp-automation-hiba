import os
from dotenv import load_dotenv
from bot.database import Database
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_connection():
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    print(f"🔌 Testing connection to: {db_url}")
    
    try:
        db = Database()
        # Try to get a session and run a simple query
        session = db.get_session()
        result = session.execute(text("SELECT 1")).scalar()
        print(f"✅ Connection successful! Result: {result}")
        session.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    verify_connection()
