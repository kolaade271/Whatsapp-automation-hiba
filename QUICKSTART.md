# 🚀 WafR WhatsApp Chatbot - Quick Start Guide

## ✅ Server Status

Your FastAPI WhatsApp chatbot is **RUNNING** on:
- **URL**: http://localhost:8000
- **Status**: ✅ Healthy
- **Active Sessions**: 0

## 📁 Project Structure

```
whatsapp_bot/
├── main.py                      # ✅ FastAPI app (RUNNING)
├── bot/
│   ├── webhook.py               # Webhook handlers
│   ├── flow_handler.py          # Conversation flow logic
│   ├── session_manager.py       # Session management
│   ├── messages.py              # Bilingual messages
│   └── whatsapp_client.py       # WhatsApp API client
├── test_flow.py                 # Automated flow test
├── interactive_test.py          # Manual interactive test
├── requirements.txt
├── .env.example
└── README.md
```

## 🧪 Testing the Flow

### Option 1: Interactive Test (Recommended for Quick Testing)

```bash
cd /Users/adekola/Documents/Upwork/Hiba/whatsapp_bot
source venv/bin/activate
python interactive_test.py
```

Then follow the conversation:
1. Type: `Hi` → Bot shows language selection
2. Type: `1` → Select French
3. Type: `1` → Select IAM recharge
4. Type: `06 12 34 56 78` → Enter phone
5. Type: `6` → Select 50 DH
6. Type: `5` → Select Pass Internet
7. Type: `Confirmer` → Confirm transaction

### Option 2: API Endpoints

Test the API directly:

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Test webhook verification (for WhatsApp setup)
curl "http://localhost:8000/webhook/?hub.mode=subscribe&hub.verify_token=YOUR_VERIFY_TOKEN_HERE&hub.challenge=test123"
```

## 🔌 Connecting to WhatsApp Business API

### Step 1: Get WhatsApp Credentials

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create/select your app
3. Add **WhatsApp** product
4. Get your credentials:
   - **Access Token** (from API Setup)
   - **Phone Number ID** (from API Setup)
   - **Create a Verify Token** (any random string you choose)

### Step 2: Configure Environment

```bash
cd /Users/adekola/Documents/Upwork/Hiba/whatsapp_bot
cp .env.example .env
```

Edit `.env`:
```env
WHATSAPP_ACCESS_TOKEN=your_actual_token_here
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=your_custom_verify_token_here
```

### Step 3: Expose Your Server (for Webhook)

**For Development (using ngrok):**
```bash
# Install ngrok if you don't have it
brew install ngrok

# Expose your local server
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

**For Production:**
Deploy to a server with a public domain (Heroku, Railway, DigitalOcean, etc.)

### Step 4: Configure Webhook in Meta

1. In Meta dashboard → WhatsApp → Configuration
2. Set **Webhook URL**: `https://your-domain.com/webhook/`
3. Set **Verify Token**: Same as in your `.env`
4. Subscribe to field: `messages`
5. Click **Verify and Save**

### Step 5: Update WhatsApp Client

Edit `bot/webhook.py` line 22:
```python
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "YOUR_VERIFY_TOKEN_HERE")
```

Change to:
```python
VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")
```

## 📊 Current Conversation Flow

### French Flow (Option 1)
```
User: Hi
Bot: Language selection (1=French, 2=Arabic)

User: 1
Bot: Service menu (1-9)

User: 1 (IAM Recharge)
Bot: Enter phone number

User: 06 XX XX XX XX
Bot: Select amount (5-300 DH)

User: 6 (50 DH)
Bot: Select offer (12 options)

User: 5 (Pass Internet)
Bot: Confirmation summary

User: Confirmer
Bot: ✅ Success message
```

### Arabic Flow (Option 2)
```
User: مرحبا
Bot: Language selection

User: 2
Bot: Service menu (10-18)

User: 10 (IAM)
Bot: Enter phone

User: 06 XX XX XX XX
Bot: Select amount

User: 7 (100 DH)
Bot: Select offer

User: 5 (Pass Internet)
Bot: Confirmation

User: تأكيد
Bot: ✅ Success
```

## 🔧 Next Steps

### 1. Implement Payment Integration

Edit `bot/flow_handler.py` → `_process_recharge()` method (line 161):

```python
def _process_recharge(self, session: UserSession) -> Dict:
    """Process the actual recharge"""
    
    # 1. Check user wallet balance
    # user_balance = get_user_balance(session.phone_number)
    # if user_balance < float(session.data["amount"]):
    #     return {"success": False, "error": "insufficient_balance"}
    
    # 2. Call operator API
    # result = call_operator_api(
    #     operator=session.data["operator"],
    #     phone=session.data["phone"],
    #     amount=session.data["amount"],
    #     offer=session.data["offer"]
    # )
    
    # 3. Deduct from wallet
    # deduct_from_wallet(session.phone_number, amount)
    
    # 4. Store transaction
    # save_transaction(session.data)
    
    return {"success": True, "transaction_id": "TXN123456"}
```

### 2. Add Database

Install database library:
```bash
source venv/bin/activate
pip install sqlalchemy psycopg2-binary  # For PostgreSQL
# OR
pip install pymongo  # For MongoDB
```

Create models for:
- Users
- Transactions
- Wallet balances

### 3. Add Error Handling

- Insufficient balance
- Operator API failures
- Network timeouts
- Invalid inputs

### 4. Add Logging & Monitoring

- Transaction logs
- Error tracking
- User analytics
- Performance monitoring

## 📝 Available Commands

```bash
# Start server
cd /Users/adekola/Documents/Upwork/Hiba/whatsapp_bot
source venv/bin/activate
python main.py

# Interactive test
python interactive_test.py

# Check server status
curl http://localhost:8000/health

# View logs
# (Check terminal where server is running)
```

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>
```

### Import errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt
```

### WhatsApp webhook not working
1. Check ngrok is running
2. Verify webhook URL in Meta dashboard
3. Check verify token matches
4. Look at server logs for errors

## 📚 Documentation

- [WhatsApp Business API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Project README](README.md)

## ✅ What's Working

- ✅ FastAPI server running
- ✅ Session management
- ✅ Complete conversation flow (French & Arabic)
- ✅ Webhook endpoints ready
- ✅ Message templates
- ✅ WhatsApp API client

## ⏳ What Needs Implementation

- ⏳ WhatsApp API credentials configuration
- ⏳ Payment/recharge API integration
- ⏳ Database for transactions
- ⏳ User wallet system
- ⏳ Error handling & retries
- ⏳ Production deployment

## 🗄️ Database

The bot uses a local SQLite database (`wafr_bot.db`) to store:
- **Users:** Phone number, language, wallet balance
- **Transactions:** History of all recharges

### Viewing Data
You can use any SQLite viewer or the command line:

```bash
sqlite3 wafr_bot.db
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM transactions;
```

### Initial Balance
New users automatically get **1000 DH** welcome bonus for testing purposes.

---

## 🚀 Deployment

---

**Need help?** Check the logs in the terminal where the server is running!
