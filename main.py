import telebot
import os
import threading
import urllib.parse
from flask import Flask
from telebot.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# ⚙️ CONFIGURATION (ማስተካከያ)
# ==========================================
TOKEN = '8570666490:AAHkzva23guJaWJRn2bUoV2ahI54T9PAtGs' 
DOMAIN = 'https://royalspin.wuaze.com'  
CHANNEL_LINK = 'https://t.me/afro_game' 
SUPPORT_USER = 'https://t.me/afro_game' 

# ለቦቱ የሚሆን ማራኪ ምስል (Banner)
# ማሳሰቢያ፡ ይህ ሊንክ በቀጥታ ምስል መሆን አለበት (.jpg/.png)
BANNER_IMG = "https://img.freepik.com/free-vector/casino-games-design_1212-368.jpg"

# ==========================================

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER (Render ላይ ቦቱ እንዳይዘጋ ይጠብቀዋል) ---
@app.route('/')
def home():
    return "🔥 AFRO GAMES BOT IS RUNNING! 🔥"

def run_web():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# --- LINK GENERATOR ---
# ተጫዋቹ "Play" ሲል መረጃውን ወደ PHP ይልካል
def get_game_url(user_id, name):
    safe_name = urllib.parse.quote(name)
    # ይህ ሊንክ ወደ index.php ይወስዳል፣ tg_id እና ስም ይዞ ይሄዳል
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
        
        # 1. ሊንኮችን ማዘጋጀት
        game_link = get_game_url(user_id, first_name)
        wallet_link = get_wallet_url(user_id)

        # 2. ቋሚ የሆነ ሜኑ በተን (Persistent Menu Button)
        try:
            bot.set_chat_menu_button(
                chat_id=chat_id,
                menu_button=MenuButtonWebApp(type="web_app", text="🎮 PLAY NOW", web_app=WebAppInfo(url=game_link))
            )
        except: pass

        # 3. የሚያምሩ በተኖች (Inline Keyboard)
        markup = InlineKeyboardMarkup()
        
        # ትልቅ የመጫወቻ በተን
        btn_play = InlineKeyboardButton("🚀 ወደ ጨዋታው ይግቡ (PLAY) 🚀", web_app=WebAppInfo(url=game_link))
        markup.row(btn_play)
        
        # የኪስ ቦርሳ እና ቻናል
        btn_wallet = InlineKeyboardButton("💰 ሂሳብ (Wallet)", web_app=WebAppInfo(url=wallet_link))
        btn_channel = InlineKeyboardButton("📢 ቻናል (Channel)", url=CHANNEL_LINK)
        markup.row(btn_wallet, btn_channel)
        
        # እገዛ
        btn_support = InlineKeyboardButton("💬 እገዛ (Support)", url=SUPPORT_USER)
        markup.row(btn_support)

        # 4. የሚስብ ጽሁፍ (Caption)
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

        # 5. ምስሉን እና ጽሁፉን መላክ
        bot.send_photo(
            chat_id, 
            BANNER_IMG, 
            caption=caption_text, 
            parse_mode="HTML", 
            reply_markup=markup
        )

    except Exception as e:
        print(f"Error: {e}")
        # ምስል ካልሰራ ጽሁፍ ብቻ ይላክ
        bot.send_message(message.chat.id, "Welcome to Afro Games! Click Play below.", reply_markup=markup)

# --- START THE BOT ---
if __name__ == "__main__":
    # Web Server በ Background ይሮጣል
    t = threading.Thread(target=run_web)
    t.start()
    
    # Bot ይጀምራል
    print("✅ Bot started with Pro Design...")
    bot.infinity_polling()
