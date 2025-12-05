# 🐬 Setting Up MySQL for WafR Bot

Your bot is now configured to use **SQLAlchemy**, which supports both SQLite (default) and MySQL.

## 1. Prerequisites

Make sure you have a MySQL server running. You can use:
- **Local MySQL Server** (installed via Homebrew, XAMPP, etc.)
- **Cloud MySQL** (AWS RDS, DigitalOcean, Railway, etc.)

## 2. Create Database

Log in to your MySQL server and create a database:

```sql
CREATE DATABASE wafr_bot;
```

## 3. Configure .env

Open your `.env` file and update the `DATABASE_URL` variable.

**Format:**
```
mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
```

**Example (Local):**
```ini
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/wafr_bot
```

**Example (Cloud):**
```ini
DATABASE_URL=mysql+pymysql://admin:securepass@db.example.com:3306/wafr_bot
```

## 4. Run the Bot

Restart your bot. SQLAlchemy will automatically connect to MySQL and create the necessary tables (`users` and `transactions`) if they don't exist.

```bash
python main.py
```

## 5. Verify Connection

Check the logs when the bot starts. You should see:
```
INFO: Database connected: mysql+pymysql
```

---

## ⚠️ Troubleshooting

**Error: `ModuleNotFoundError: No module named 'pymysql'`**
Run: `pip install pymysql` (It should be installed already)

**Error: `Can't connect to MySQL server`**
- Check if MySQL is running
- Verify host, port, username, and password
- Ensure the database `wafr_bot` exists
