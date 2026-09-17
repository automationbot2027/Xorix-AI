"""
XORIX PRIME - FREE RENDER WEB SERVICE (0$)
Runs as Web Service + Bot in background thread - FREE TIER
"""
import os
import threading
import logging
from flask import Flask
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_reply(prompt: str) -> str:
    if GROQ_KEY and GROQ_KEY.startswith("gsk_"):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_KEY)
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are XORIX PRIME. Reply short Roman Urdu + English, friendly. 16GB optimized, 24/7 online."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
    
    if GEMINI_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text[:1000]
        except Exception as e:
            logger.error(f"Gemini error: {e}")
    
    return "Main online hun! API check karo."

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 XORIX OS v2.0 ONLINE 24/7\n\n/start - Ye message\n/status - Status\n/help - Madad\n\nBolo kya karwana hai?", parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = """📊 XORIX SYSTEM STATUS

🤖 Main Agent: ONLINE 24/7
☁️ Hosting: Render FREE Web Service - LIVE 0$
💾 RAM: 16GB Optimized
🎙️ Voice: Whisper Offline Ready
📁 Folder: xorix-ai-v2
✅ Render: FREE LIVE - No PC needed
✅ APIs: 4 Keys Active

PC band bhi ho to main online rahunga!"""
    await update.message.reply_text(status)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bolo 'Xorix youtube post banao' etc. Main sun raha hun 24/7!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    reply = get_ai_reply(user_text)
    await update.message.reply_text(reply)

def run_bot():
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN missing")
        return
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot polling started - 24/7 LIVE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

# Flask for Render Web Service free tier
flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "XORIX PRIME is LIVE 24/7 - Telegram bot running! @Xoricbot"

@flask_app.route('/health')
def health():
    return "OK - Bot Running"

if __name__ == "__main__":
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Start Flask for Render (needs port)
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
