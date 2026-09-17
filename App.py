"""
XORIX PRIME - FINAL THREAD FIX 2026-09-17 - 24/7 NO SLEEP
Fixes: set_wakeup_fd only works in main thread - by running Flask in background thread, Bot in MAIN thread
This fixes the crash loop seen in Render logs
"""
import os
import threading
import logging
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

print(f"TOKEN CHECK: TELEGRAM={'SET' if TELEGRAM_TOKEN else 'MISSING'}")

def get_ai_reply(prompt: str) -> str:
    if GROQ_KEY and GROQ_KEY.startswith("gsk_"):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_KEY)
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are XORIX PRIME. Reply short Roman Urdu + English, friendly. 24/7 online."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
    if GEMINI_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_KEY)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text[:1000]
        except Exception as e:
            logger.error(f"Gemini error: {e}")
    return "Main online hun! Bolo kya kaam hai? (Render Live 24/7 Fixed)"

# Flask app - will run in BACKGROUND thread
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "XORIX PRIME is LIVE 24/7 FREE - Models 2026 - @Xoricbot - gpt-oss-20b + gemini-2.5-flash - Thread Fix ON"

@flask_app.route('/health')
def health():
    return "OK - Bot Running - Thread Fix - 24/7"

@flask_app.route('/ping')
def ping():
    return "PONG - Alive - Thread Fix"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting Flask on port {port} in background thread")
    # use_reloader=False to avoid double start
    flask_app.run(host="0.0.0.0", port=port, use_reloader=False)

# Start Flask in background thread FIRST
flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
logger.info("Flask thread started in background - Bot will run in MAIN thread")

# Now run Telegram bot in MAIN thread (fixes set_wakeup_fd error)
if not TELEGRAM_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN missing! Set it in Render Environment")
    # Keep Flask alive even without token
    import time
    while True:
        time.sleep(60)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🚀 XORIX OS v2.0 ONLINE 24/7 FREE - THREAD FIXED\n\nBot is LIVE on Render!\n/start - Menu\n/status - Status\n\nBolo kya karwana hai?")

    async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📊 XORIX STATUS - THREAD FIXED\n\n🤖 ONLINE 24/7 FREE\n☁️ Render + Cron 1min - LIVE\n✅ Models: gpt-oss-20b + gemini-2.5-flash\n✅ Fix: set_wakeup_fd fixed\n\nPC band bhi ho to online!")

    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        logger.info(f"Telegram msg: {user_text}")
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        reply = get_ai_reply(user_text)
        await update.message.reply_text(reply)

    logger.info("Starting Telegram bot polling in MAIN thread...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Bot polling started - 24/7 LIVE - Thread Fixed")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

except Exception as e:
    logger.error(f"Fatal bot error: {e}")
    import time
    while True:
        time.sleep(60)
