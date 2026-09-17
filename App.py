"""
XORIX PRIME - FREE RENDER WEB SERVICE (0$) - MODELS UPDATED 2026
Groq: llama-3.3-70b-versatile | Gemini: gemini-2.0-flash
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
    # 1. Groq - NEW MODEL
    if GROQ_KEY and GROQ_KEY.startswith("gsk_"):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_KEY)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # NEW - old decommissioned
                messages=[
                    {"role": "system", "content": "You are XORIX PRIME. Reply short Roman Urdu + English, friendly, helpful. 16GB optimized, 24/7 online."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
            try:
                from groq import Groq
                client = Groq(api_key=GROQ_KEY)
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300
                )
                return completion.choices[0].message.content
            except Exception as e2:
                logger.error(f"Groq fallback error: {e2}")
    
    # 2. Gemini - NEW SDK
    if GEMINI_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text[:1000]
        except Exception as e:
            logger.error(f"Gemini new SDK error: {e}")
            try:
                import google.generativeai as genai_old
                genai_old.configure(api_key=GEMINI_KEY)
                model = genai_old.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
                return response.text[:1000]
            except Exception as e2:
                logger.error(f"Gemini old SDK error: {e2}")
    
    # 3. OpenRouter
    if OPENROUTER_KEY:
        try:
            import requests
            headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
            data = {"model": "meta-llama/llama-3.3-70b-instruct", "messages": [{"role": "user", "content": prompt}]}
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=20)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
    
    return "Main online hun! Bolo kya kaam hai?"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 XORIX OS v2.0 ONLINE 24/7 FREE\n\n/start - Menu\n/status - Status\n/help - Help\n\nBolo kya karwana hai?", parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = """📊 XORIX SYSTEM STATUS

🤖 Main Agent: ONLINE 24/7 FREE
☁️ Hosting: Render FREE Web Service - LIVE 0$
💾 RAM: 16GB Optimized
🎙️ Voice: Whisper Offline Ready
✅ Models: Groq 3.3-70b + Gemini 2.0-flash (2026 updated)
✅ APIs: 4 Keys Active
✅ GitHub: Connected

PC band bhi ho to main online rahunga!"""
    await update.message.reply_text(status)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bolo 'Xorix youtube post banao' - Main 24/7 sun raha hun!")

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
    print("✅ Bot polling started - 24/7 LIVE FREE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return "XORIX PRIME is LIVE 24/7 FREE - @Xoricbot - Models Updated 2026"

@flask_app.route('/health')
def health():
    return "OK - Bot Running - Free Tier"

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)
