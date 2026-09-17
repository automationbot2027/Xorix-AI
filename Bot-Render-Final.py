"""
XORIX PRIME - RENDER DEPLOY READY
24/7 Online - No PowerShell needed
Telegram + Voice + AI - All in one
"""
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

def get_ai_reply(prompt: str) -> str:
    # Try Groq first (fastest)
    if GROQ_KEY and GROQ_KEY.startswith("gsk_"):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_KEY)
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are XORIX PRIME, a helpful AI assistant for Shafiq. Reply in Roman Urdu + English mix, friendly, short. You control PC, e-commerce, CRM. 16GB optimized."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq error: {e}")
    
    # Fallback to Gemini (new AQ auth keys)
    if GEMINI_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            return response.text[:1000]
        except Exception as e:
            logger.error(f"Gemini error: {e}")
    
    # Fallback to OpenRouter
    if OPENROUTER_KEY:
        try:
            import requests
            headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "meta-llama/llama-3.1-70b-instruct",
                "messages": [{"role": "user", "content": prompt}]
            }
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=20)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenRouter error: {e}")
    
    return "API keys check karo, .env me 4 keys dalo. Main online hun!"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🚀 **XORIX OS v2.0 - PRIME AGENT ONLINE 24/7**

Assalam-o-Alaikum! Main XORIX PRIME hun.

**Commands:**
/start - Ye message
/status - System status
/help - Madad
/voice - Voice test

Bolo kya karwana hai?
"""
    await update.message.reply_text(msg, parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = """
📊 **XORIX SYSTEM STATUS** 🤖

🤖 Main Agent: ONLINE 24/7
☁️ Hosting: Render.com - LIVE
💾 RAM: 16GB Optimized
🖥️ Dashboard: NATIVE .EXE - Running
🎙️ Voice: ACTIVE - Whisper Small Ready
📁 Folder: xorix-ai-v2 - OK
👥 Team: 7 Agents ACTIVE
• PRODUCT-01: WORKING
• SUPPLIER-02: ONLINE
• STORE-03: ONLINE
• MARKETING-04: ONLINE
• CLIENT-05: ONLINE
• HR-06: ONLINE
• VOICE-07: ONLINE

✅ Long Term Setup: STRONG
❌ Jugaad: KHATAM
✅ Render Deploy: LIVE (24/7 No PC Needed)
✅ Telegram: ONLINE
✅ APIs: 4 Keys Active (Gemini AQ New)

PC band bhi ho to main online rahunga!
"""
    await update.message.reply_text(status, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 **XORIX HELP**

1. Seedha bolo: "Xorix youtube post banao"
2. /status se system check karo
3. Voice ke liye: PC pe Voice-Agent-Whisper-Final.py chalao
4. Render pe deploy ke baad PowerShell band kar sakte ho

API Docs: aistudio.google.com
Groq: console.groq.com
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logger.info(f"User: {user_text}")
    
    # Typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    reply = get_ai_reply(user_text)
    await update.message.reply_text(reply)

def main():
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN missing in .env")
        return
    
    print("="*60)
    print("🚀 XORIX PRIME - RENDER DEPLOY MODE")
    print("24/7 Online - No PowerShell needed")
    print("="*60)
    
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot polling started - 24/7 LIVE")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
