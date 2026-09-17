"""
XORIX PRIME - FINAL WITH CLOUD DASHBOARD - ACCESS FROM ANYWHERE
PC ghar pe, Office se bhi dashboard kholo - https://xorix-ai.onrender.com/dashboard
Fixes: set_wakeup_fd + Cloud Dashboard + API Chat
"""
import os
import threading
import logging
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

def get_ai_reply(prompt: str):
    if GROQ_KEY and GROQ_KEY.startswith("gsk_"):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_KEY)
            completion = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are XORIX PRIME - 24/7 Cloud Agent. Reply short Roman Urdu + English. You work from anywhere - PC, Telegram, Online Dashboard."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )
            return completion.choices[0].message.content, "gpt-oss-20b"
        except Exception as e:
            logger.error(f"Groq error: {e}")
    if GEMINI_KEY:
        try:
            from google import genai
            client = genai.Client(api_key=GEMINI_KEY)
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
            return response.text[:1000], "gemini-2.5-flash"
        except Exception as e:
            logger.error(f"Gemini error: {e}")
    return "Main online hun 24/7! PC ghar pe bhi, office se bhi kaam karunga.", "fallback"

flask_app = Flask(__name__)

# Enable CORS for dashboard from anywhere
@flask_app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

@flask_app.route('/')
def home():
    return """XORIX PRIME is LIVE 24/7 FREE - Models 2026 - @Xoricbot - gpt-oss-20b + gemini-2.5-flash - Thread Fix ON<br><br>
    <b>Dashboard:</b> <a href="/dashboard">https://xorix-ai.onrender.com/dashboard</a> - Open from anywhere (Office/Home)<br>
    <b>Telegram:</b> @Xoricbot - 24/7<br>
    <b>Health:</b> <a href="/health">/health</a>"""

@flask_app.route('/health')
def health():
    return "OK - Bot Running - Thread Fix - 24/7 - Dashboard Active"

@flask_app.route('/ping')
def ping():
    return "PONG - Alive"

@flask_app.route('/api/chat', methods=['POST', 'OPTIONS'])
def api_chat():
    if request.method == 'OPTIONS':
        return '', 200
    data = request.get_json()
    message = data.get('message', '') if data else ''
    logger.info(f"Cloud Dashboard msg: {message}")
    reply, model = get_ai_reply(message)
    return jsonify({"reply": reply, "model": model})

@flask_app.route('/dashboard')
def dashboard():
    # Cloud Dashboard - Access from anywhere, no laptop needed
    return """
<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>XORIX OS v2.0 - CLOUD DASHBOARD - Access from Anywhere</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#050507;color:#e0e0e0;font-family:monospace;height:100vh;overflow:hidden}
.message{margin:12px;padding:16px 20px;border-radius:16px;max-width:80%;word-wrap:break-word}
.msg-user{margin-left:auto;background:linear-gradient(135deg, rgba(0,255,240,0.15), rgba(0,217,255,0.1));border:1px solid rgba(0,255,240,0.4)}
.msg-agent{background:linear-gradient(135deg, rgba(255,0,255,0.12), rgba(138,43,226,0.1));border:1px solid rgba(255,0,255,0.3)}
.input-bar{display:flex;gap:12px;padding:16px;background:rgba(0,0,0,0.6);border-top:1px solid rgba(0,255,240,0.2)}
.input-bar input{flex:1;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:14px 18px;color:#fff;outline:none}
.btn{padding:12px 20px;border-radius:12px;border:1px solid rgba(0,255,240,0.3);background:rgba(0,255,240,0.1);color:#00FFF0;cursor:pointer;font-weight:bold}
</style></head>
<body>
<div style="display:flex;height:100vh;flex-direction:column">
  <div style="padding:16px 24px;border-bottom:1px solid rgba(0,255,240,0.2);background:rgba(0,0,0,0.4);display:flex;justify-content:space-between">
    <div><span style="color:#00FFF0;font-weight:bold">XORIX OS v2.0 - CLOUD DASHBOARD</span> - Access from Anywhere (Office/Home)</div>
    <div style="font-size:11px">Render LIVE + Telegram @Xoricbot + Cron 1min = 0 sec sleep | <span style="color:#00FF88">Thread Fixed ON</span></div>
  </div>
  <div id="chat-box" style="flex:1;overflow-y:auto;padding:24px;display:flex;flex-direction:column;gap:16px">
    <div class="message msg-agent">
      <div style="font-size:11px;color:#FF00FF;margin-bottom:8px">XORIX PRIME • CLOUD DASHBOARD • 24/7</div>
      <div>Assalam-o-Alaikum! Ye <b>Cloud Dashboard</b> hai - <b>https://xorix-ai.onrender.com/dashboard</b><br><br>
      <b>Faida:</b> Laptop ghar pe hai, office se is link ko kholo to bhi kaam karega! PC ki zarurat nahi.<br>
      <b>Telegram:</b> @Xoricbot bhi 24/7 live hai<br>
      <b>PC Dashboard:</b> Ghar pe jab PC on ho to wahan bhi active<br><br>
      Yahan message likho, direct AI reply ayega (gpt-oss-20b + gemini-2.5-flash) 🚀</div>
    </div>
  </div>
  <div class="input-bar">
    <input type="text" id="user-input" placeholder="Type here... Office se bhi kaam karega!" onkeypress="if(event.key==='Enter') sendMessage()" />
    <button class="btn" onclick="sendMessage()">SEND ➤</button>
  </div>
</div>
<script>
async function sendMessage(){
  const input=document.getElementById('user-input');
  const text=input.value.trim(); if(!text) return;
  const box=document.getElementById('chat-box');
  const u=document.createElement('div'); u.className='message msg-user'; u.innerHTML='<div>'+text+'</div>'; box.appendChild(u); input.value='';
  const a=document.createElement('div'); a.className='message msg-agent'; a.innerHTML='<div>Sooch raha hoon... '+text+'</div>'; box.appendChild(a); box.scrollTop=box.scrollHeight;
  try{
    const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
    const data=await res.json();
    a.innerHTML='<div style="font-size:11px;color:#FF00FF;margin-bottom:8px">XORIX PRIME • '+data.model+' • CLOUD</div><div>'+data.reply.replace(/\\n/g,'<br>')+'</div>';
  }catch(e){ a.innerHTML='<div>Error: '+e+'</div>'; }
  box.scrollTop=box.scrollHeight;
}
</script>
</body></html>
    """

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Starting Flask on port {port} in background")
    flask_app.run(host="0.0.0.0", port=port, use_reloader=False)

flask_thread = threading.Thread(target=run_flask, daemon=True)
flask_thread.start()
logger.info("Flask thread started - Bot in MAIN thread")

if not TELEGRAM_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN missing!")
    import time
    while True: time.sleep(60)

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🚀 XORIX OS v2.0 ONLINE 24/7 - CLOUD DASHBOARD ACTIVE\\n\\nDashboard: https://xorix-ai.onrender.com/dashboard - Office se bhi kholo!\\nTelegram: 24/7 Live\\nPC Dashboard bhi active\\n\\nBolo kya karwana hai?")
    async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📊 STATUS\\n\\n✅ Render: LIVE Thread Fixed\\n✅ Telegram: @Xoricbot LIVE\\n✅ Cloud Dashboard: /dashboard - Office se bhi\\n✅ Cron 1min + Uptime 5min = 0 sleep\\n\\nPC ghar pe ho to bhi cloud se kaam karega!")
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_text = update.message.text
        logger.info(f"Telegram msg: {user_text}")
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        reply, _ = get_ai_reply(user_text)
        await update.message.reply_text(reply)
    logger.info("Starting Telegram bot in MAIN thread...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("✅ Bot polling started - Thread Fixed + Cloud Dashboard")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
except Exception as e:
    logger.error(f"Fatal: {e}")
    import time
    while True: time.sleep(60)
