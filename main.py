import sqlite3
import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.account import UpdateStatusRequest

# Credentials
API_ID = 3097929 #AHAPE TG ACCOUNT API DALE
API_HASH = '7baacc76eb2a6f4e530318f039bd1dc3' #PASTE YOUR API HASH 

FIRST_TIME_TEXT = """
👋 WELCOME!

✅ Thanks For Contacting Us

💎 Rare Accounts Available
🎁 Exclusive Codes Available
⚡ Fast & Trusted Service

📢 Official Channel:
🔗 @public_120

⏳ Please Wait For Admin Reply.
"""

OFFLINE_TEXT = """
👋 HEY! I'M CURRENTLY OFFLINE ☠️

🔗 JOIN THE CHANNEL:- @public_120

☠️ YOU CAN BUY RARE ACC & CODES ☑️

IF YOU WANT TO BUY SOMETHING 💰
"""

conn = sqlite3.connect('chat_tracker.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)'
)
conn.commit()

client = TelegramClient(
    'hybrid_bot_session',
    API_ID,
    API_HASH
)

@client.on(events.NewMessage(incoming=True))
async def handle_replies(event):
    if not event.is_private:
        return

    user_id = event.sender_id

    cursor.execute(
        'SELECT user_id FROM users WHERE user_id = ?',
        (user_id,)
    )
    is_existing_user = cursor.fetchone()

    if not is_existing_user:
        cursor.execute(
            'INSERT INTO users (user_id) VALUES (?)',
            (user_id,)
        )
        conn.commit()

        await event.respond(FIRST_TIME_TEXT)
        print(f"⚡ Fresh Chat Welcome Sent to: {user_id}")
        return

    try:
        await client(UpdateStatusRequest(offline=False))

        await event.respond(OFFLINE_TEXT)
        print(f"☠️ Offline Reply Sent to: {user_id}")

        await asyncio.sleep(0.5)

        await client(UpdateStatusRequest(offline=True))

    except Exception as e:
        print(f"Error handling status: {e}")

print("TELEGRAM AUTO REPLY BOT IS STARTED ONWER BY @public_120...")

client.start()
client.run_until_disconnected()