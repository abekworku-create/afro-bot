import telebot
import os
import threading
import urllib.parse
from flask import Flask
from waitress import serve
from telebot.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TOKEN = '8570666490:AAHkzva23guJaWJRn2bUoV2ahI54T9PAtGs' 
DOMAIN = 'https://royalspin.wuaze.com'  
CHANNEL_LINK = 'https://t.me/afro_game' 
SUPPORT_USER = 'https://t.me/afro_game' 
BANNER_IMG = "https://gemini.google.com/share/9783d8a6f35a"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER ---
@app.route('/')
def home():
    return "🔥 AFRO GAMES BOT IS RUNNING! (Production Mode) 🔥"

def run_web():
    port = int(os.environ.get('PORT', 8080))
    serve(app, host="0.0.0.0", port=port)

# --- HELPER FUNCTIONS ---
def get_game_url(user_id, name):
    safe_name = urllib.parse.quote(name)
    return f"{DOMAIN}/index.php?tg_id={user_id}&name={safe_name}"

def get_wallet_url(user_id):
    return f"{DOMAIN}/wallet.php?tg_id={user_id}"

# ==========================================
# 🔥 PRO DESIGN HANDLERS
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
        btn_wallet = InlineKeyboardButton("💰 ሂሳብ (Wallet)", web_app=WebAppInfo(url=wallet_link))
        btn_channel = InlineKeyboardButton("📢 ቻናል (Channel)", url=CHANNEL_LINK)
        markup.row(btn_wallet, btn_channel)
        btn_support = InlineKeyboardButton("💬 እገዛ (Support)", url=SUPPORT_USER)
        markup.row(btn_support)

        caption_text = (
            f"👋 <b>ሰላም {first_name}!</b>\n\n"
            "ወደ <b>AFRO GAMES</b> እንኳን በደህና መጡ! 🏆\n\n"
            "🎰 <b>የሚገኙ ጨዋታዎች፡</b>\n"
            "• Spin & Win 🎡\n"
            "• Crash / Aviator 🚀\n"
            "• Sport Betting ⚽\n"
            "• Mines 💣\n\n"
            "✅ <b>ፈጣን ክፍያ | አስተማማኝ | አዝናኝ</b>\n\n"
            "👇 <b>ለመጀመር ከታች ያለውን በተን ይጫኑ!</b>"
        )

        bot.send_photo(chat_id, BANNER_IMG, caption=caption_text, parse_mode="HTML", reply_markup=markup)

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "Welcome! Click Play below.", reply_markup=markup)

# --- START ---
if __name__ == "__main__":
    # Web Server ማስጀመር
    t = threading.Thread(target=run_web)
    t.start()
    
    print("✅ Removing old webhooks...")
    # 🔥 ይህ በጣም ወሳኝ ነው! የድሮውን Webhook በግድ ያጠፋዋል 🔥
    bot.delete_webhook()
    
    print("✅ Production Bot Started...")
    bot.infinity_polling()
