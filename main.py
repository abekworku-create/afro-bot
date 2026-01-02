import telebot
import os
import time
from flask import Flask, request
from telebot.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TOKEN = '8570666490:AAH08os9NH0oBwYPFaZ49kVEY6e56lTn7hk' 
DOMAIN = 'https://royalspin.wuaze.com' 
CHANNEL_LINK = 'https://t.me/afro_game'
SUPPORT_USER = 'https://t.me/afro_game'
BANNER_IMG = "https://gemini.google.com/share/508fab1dec30"

# Render የሚሰጠው የራስህ የቦት ሊንክ (አንተ መቀየር አለብህ!)
# ምሳሌ: https://afro-bot.onrender.com (የ Render ዳሽቦርድ ላይ ታገኘዋለህ)
WEBHOOK_URL_BASE = "https://afro-bot.onrender.com" 
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER & WEBHOOK HANDLER ---
# ይህ ከ Polling ይልቅ Webhook ይጠቀማል (ግጭትን ያስወግዳል)
@app.route('/', methods=['GET'])
def index():
    return "🔥 AFRO GAMES BOT IS RUNNING (Webhook Mode)! 🔥"

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 403

# --- HELPER FUNCTIONS ---
def get_game_url(user_id, name):
    import urllib.parse
    safe_name = urllib.parse.quote(name)
    return f"{DOMAIN}/index.php?tg_id={user_id}&name={safe_name}"

def get_wallet_url(user_id):
    return f"{DOMAIN}/wallet.php?tg_id={user_id}"

# ==========================================
# 🔥 HANDLERS
# ==========================================
@bot.message_handler(commands=['start'])
def send_main_menu(message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name if message.from_user.first_name else "Gamer"
        chat_id = message.chat.id
        
        game_link = get_game_url(user_id, first_name)
        wallet_link = get_wallet_url(user_id)

        try:
            bot.set_chat_menu_button(
                chat_id=chat_id,
                menu_button=MenuButtonWebApp(type="web_app", text="🎮 PLAY NOW", web_app=WebAppInfo(url=game_link))
            )
        except: pass

        markup = InlineKeyboardMarkup()
        btn_play = InlineKeyboardButton("🚀 ወደ ጨዋታው ይግቡ (PLAY) 🚀", web_app=WebAppInfo(url=game_link))
        markup.row(btn_play)
        markup.row(InlineKeyboardButton("💰 ሂሳብ (Wallet)", web_app=WebAppInfo(url=wallet_link)), InlineKeyboardButton("📢 ቻናል", url=CHANNEL_LINK))
        markup.row(InlineKeyboardButton("💬 እገዛ (Support)", url=SUPPORT_USER))

        caption = f"👋 <b>ሰላም {first_name}!</b>\n\nወደ <b>AFRO GAMES</b> እንኳን በደህና መጡ! 🏆\n\n👇 <b>ለመጫወት ይግቡ!</b>"
        
        bot.send_photo(chat_id, BANNER_IMG, caption=caption, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print(e)

# --- START ---
if __name__ == "__main__":
    # Webhook ማዋቀር
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    
    print("✅ Webhook Set & Server Starting...")
    
    # Start Flask Server
    from waitress import serve
    port = int(os.environ.get('PORT', 8080))
    serve(app, host="0.0.0.0", port=port)

