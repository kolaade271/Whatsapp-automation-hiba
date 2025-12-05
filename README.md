# WafR WhatsApp Chatbot

FastAPI-based WhatsApp chatbot for mobile recharge and wallet operations with bilingual support (French & Arabic).

## Features

- ✅ Bilingual conversation flow (French & Arabic)
- ✅ Session management with automatic cleanup
- ✅ Multi-step recharge process
- ✅ Support for IAM, INWI, and ORANGE operators
- ✅ Multiple recharge amounts and offers
- ✅ Transaction confirmation flow
- ✅ WhatsApp Business API integration

## Project Structure

```
whatsapp_bot/
├── main.py                 # FastAPI application entry point
├── bot/
│   ├── __init__.py
│   ├── webhook.py          # Webhook handlers
│   ├── flow_handler.py     # Conversation flow logic
│   ├── session_manager.py  # User session management
│   ├── messages.py         # Message templates
│   └── whatsapp_client.py  # WhatsApp API client
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
cd whatsapp_bot
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your WhatsApp Business API credentials:
- `WHATSAPP_ACCESS_TOKEN`: Your Meta access token
- `WHATSAPP_PHONE_NUMBER_ID`: Your WhatsApp phone number ID
- `WHATSAPP_VERIFY_TOKEN`: Custom token for webhook verification

### 3. Run the Server

```bash
python main.py
```

Or with uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## WhatsApp Business API Setup

### 1. Get API Credentials

1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app or use existing one
3. Add WhatsApp product
4. Get your:
   - Access Token (from API Setup)
   - Phone Number ID (from API Setup)

### 2. Configure Webhook

1. In your Meta app dashboard, go to WhatsApp > Configuration
2. Set webhook URL: `https://your-domain.com/webhook/`
3. Set verify token (same as in your `.env`)
4. Subscribe to webhook fields: `messages`

### 3. Test Webhook

Test webhook verification:
```bash
curl -X GET "http://localhost:8000/webhook/?hub.mode=subscribe&hub.verify_token=YOUR_VERIFY_TOKEN&hub.challenge=CHALLENGE_STRING"
```

## Conversation Flow

### Step 1: Welcome
User sends any greeting → Bot responds with language selection

### Step 2: Language Selection
- `1` → French
- `2` → Arabic

### Step 3: Service Menu
**French:**
- 1-3: Recharge operators (IAM, INWI, ORANGE)
- 4-9: Coming soon services

**Arabic:**
- 10-12: Recharge operators
- 13-18: Coming soon services

### Step 4: Phone Number
User enters recipient phone number

### Step 5: Amount Selection
User selects amount (5-300 DH)

### Step 6: Offer Selection
User selects recharge offer (12 options)

### Step 7: Confirmation
Bot shows summary → User confirms or cancels

### Step 8: Result
Success or cancellation message

## API Endpoints

### GET /
Health check endpoint

### GET /health
Returns service health status and active sessions count

### GET /webhook/
Webhook verification endpoint (called by WhatsApp)

### POST /webhook/
Webhook endpoint for receiving messages (called by WhatsApp)

## Development

### Testing Locally

Use ngrok to expose your local server:

```bash
ngrok http 8000
```

Use the ngrok URL as your webhook URL in Meta dashboard.

### Logging

Logs are configured in `main.py`. Check console output for:
- Incoming messages
- Session management
- API calls
- Errors

## Next Steps

### TODO: Implement Payment Integration

In `flow_handler.py`, the `_process_recharge()` method needs to be implemented with:

1. **Wallet Balance Check**
   - Verify user has sufficient balance
   - Deduct amount from WafR wallet

2. **Operator API Integration**
   - Call IAM/INWI/ORANGE recharge API
   - Handle API responses and errors

3. **Database Integration**
   - Store transaction records
   - Update user wallet balance
   - Save transaction history

4. **Error Handling**
   - Handle insufficient balance
   - Handle operator API failures
   - Implement retry logic

### TODO: Add Database

Add database models for:
- Users
- Transactions
- Wallet balances
- Session persistence

Recommended: PostgreSQL or MongoDB

### TODO: Add Interactive Buttons

Enhance UX by using WhatsApp interactive buttons instead of number selections.

## License

Proprietary - WafR Platform
# Whatsapp-automation-hiba
