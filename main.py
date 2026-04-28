import os
import threading
import asyncio
import random
from flask import Flask
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler

# --- 1. THE MINI APP ---
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { background: #0d1117; color: white; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #161b22; border-radius: 15px; padding: 20px; border: 1px solid #30363d; }
        select, button { width: 100%; padding: 14px; margin: 10px 0; border-radius: 10px; border: none; font-size: 16px; }
        select { background: #21262d; color: white; border: 1px solid #30363d; }
        .btn { background: linear-gradient(90deg, #00d2ff, #3a7bd5); color: white; font-weight: bold; cursor: pointer; }
        #res { margin-top: 20px; font-size: 24px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <div style="color:#58a6ff; font-weight:bold; margin-bottom:10px;">BONUS: DNF483</div>
        <h3>SIGNAL AI ROBOT</h3>
        <select id="asset">
            <option>XAU/USD (GOLD) OTC</option>
            <option>EUR/USD OTC</option>
            <option>GBP/JPY OTC</option>
        </select>
        <select id="time">
            <option>10 Seconds</option>
            <option>30 Seconds</option>
            <option>1 Minute</option>
        </select>
        <button class="btn" onclick="getSignal()">⚡ GET SIGNAL</button>
        <div id="res"></div>
    </div>
    <script>
        function getSignal() {
            const r = document.getElementById('res');
            r.innerHTML = "Analysing...";
            setTimeout(() => {
                const isCall = Math.random() > 0.5;
                const dir = isCall ? "CALL ⬆️" : "PUT ⬇️";
                const col = isCall ? "#00ff88" : "#ff4d4d";
                r.innerHTML = `<span style="color:${col}">${dir}</span><br><span style="font-size:14px; color:#aaa;">Accuracy: ${Math.floor(Math.random()*5)+93}%</span>`;
            }, 1000);
        }
    </script>
</body>
</html>
"""

app = Flask(__name__)

@app.route('/')
def home():
    return HTML_CONTENT

# --- 2. THE BOT ENGINE ---
def run_bot():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("ERROR: BOT_TOKEN variable not found!")
        return

    # Use a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def start(update: Update, context):
        # Auto-detects the Render URL
        host = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')
        url = f"https://{host}"
        kbd = [[InlineKeyboardButton("🚀 OPEN SIGNALS", web_app=WebAppInfo(url=url))]]
        await update.message.reply_text("🎯 **Signal AI Robot Live**", 
                                      reply_markup=InlineKeyboardMarkup(kbd), parse_mode="Markdown")

    try:
        application = ApplicationBuilder().token(token).build()
        application.add_handler(CommandHandler("start", start))
        print("Bot is starting polling...")
        application.run_polling(drop_pending_updates=True)
    except Exception as e:
        print(f"Bot Error: {e}")

# Start Bot thread immediately
threading.Thread(target=run_bot, daemon=True).start()

# For Render's Gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
