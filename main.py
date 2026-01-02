import telebot
import os
import time
from flask import Flask, request
from telebot.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TOKEN = '8570666490:AAH08os9NH0oBwYPFaZ49kVEY6e56lTn7hk' 
DOMAIN = 'https://royalspin.wuaze.com' 
CHANNEL_LINK = 'https://t.me/afro_game'
SUPPORT_USER = 'https://t.me/afro_game'
# ለሽፋን የሚሆን ማራኪ ፎቶ (Banner)
BANNER_IMG = "https://gemini.google.com/share/508fab1dec30" 

# Render URL
WEBHOOK_URL_BASE = "https://afro-bot.onrender.com" 
WEBHOOK_URL_PATH = "/%s/" % (TOKEN)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER ---
@app.route('/', methods=['GET'])
def index():
    return "🔥 AFRO GAMES BOT IS RUNNING! 🔥"

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
def get_game_url(user_id, name, phone):
    import urllib.parse
    safe_name = urllib.parse.quote(name)
    # ስልክ ቁጥር፣ ስም እና ID አያይዞ ይልካል
    return f"{DOMAIN}/index.php?tg_id={user_id}&name={safe_name}&phone={phone}"

def get_wallet_url(user_id):
    return f"{DOMAIN}/wallet.php?tg_id={user_id}"

# ==========================================
# 🔥 HANDLERS (መልዕክቶቹ እዚህ ተሻሽለዋል)
# ==========================================

# 1. START ሲባል - ማራኪ አቀባበል እና ስልክ ቁጥር ጥያቄ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        first_name = message.from_user.first_name if message.from_user.first_name else "ወዳጄ"
        
        # ስልክ ቁጥር መጠየቂያ በተን (ትልቅና ግልጽ)
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        # "ስልክ ቁጥር ላክ" የሚለውን ጽሁፍ ሳቢ አድርገነዋል
        phone_btn = KeyboardButton(text="📱 ለመመዝገብ ይህን ይጫኑ (Register)", request_contact=True)
        markup.add(phone_btn)

        # 🔥 የተሻሻለ የእንኳን ደህና መጣችሁ ጽሁፍ 🔥
        msg = (
            f"👋 <b>ሰላም {first_name}!</b> እንኳን ወደ <b>AFRO GAMES</b> በደህና መጡ! 🇪🇹\n\n"
            f"🏆 እዚህ እጅግ አዝናኝ እና አትራፊ ጨዋታዎችን ያገኛሉ! \n"
            f"🚀 <b>Crash (Aviator)</b>\n"
            f"⚽ <b>Spin & Win</b>\n"
            f"💣 <b>Mines</b> እና ሌሎችም...\n\n"
            f"🎁 <b>ለመጀመር አካውንት መክፈት ያስፈልግዎታል።</b>\n"
            f"ከታች ያለውን <b>'📱 ለመመዝገብ ይህን ይጫኑ'</b> የሚለውን በተን ይንኩ። 👇"
        )
        
        bot.send_message(message.chat.id, msg, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print(e)

# 2. ስልክ ቁጥር ሲላክ - ደማቅ አቀባበል እና ጨዋታው
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        if message.contact is not None:
            user_id = message.from_user.id
            first_name = message.from_user.first_name if message.from_user.first_name else "Gamer"
            phone_number = message.contact.phone_number
            
            game_link = get_game_url(user_id, first_name, phone_number)
            wallet_link = get_wallet_url(user_id)

            # የ Menu Button ማስተካከል
            try:
                bot.set_chat_menu_button(
                    chat_id=message.chat.id,
                    menu_button=MenuButtonWebApp(type="web_app", text="🎮 PLAY NOW", web_app=WebAppInfo(url=game_link))
                )
            except: pass

            # 🔥 የተሻሻሉ የውስጥ በተኖች (Inline Buttons) 🔥
            markup = InlineKeyboardMarkup()
            # ዋናው የመጫወቻ በተን
            btn_play = InlineKeyboardButton("🎰 ወደ ጨዋታው ይግቡ (PLAY) 🎰", web_app=WebAppInfo(url=game_link))
            markup.row(btn_play)
            
            # ተጨማሪ አማራጮች
            markup.row(
                InlineKeyboardButton("💰 ሂሳብ (Wallet)", web_app=WebAppInfo(url=wallet_link)), 
                InlineKeyboardButton("📢 ቻናል (Join)", url=CHANNEL_LINK)
            )
            markup.row(InlineKeyboardButton("💬 እርዳታ (Support)", url=SUPPORT_USER))

            # የድሮውን ኪቦርድ እናጥፋ
            remove_kb = telebot.types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, "✅ ምዝገባዎ ተሳክቷል!", reply_markup=remove_kb)

            # 🔥 የተሻሻለ የማረጋገጫ መልዕክት 🔥
            caption = (
                f"🎉 <b>እንኳን ደስ አለዎት {first_name}!</b>\n\n"
                f"✅ አካውንትዎ በተሳካ ሁኔታ ተከፍቷል!\n"
                f"🎁 እንደ አዲስ ተመዝጋቢ <b>ነጻ 10 ብር ቦነስ</b> ተሰጥቶዎታል!\n\n"
                f"👇 <b>'ወደ ጨዋታው ይግቡ'</b> የሚለውን በመጫን አሁኑኑ መጫወት ይጀምሩ! መልካም እድል! 🍀"
            )
            
            # ባነር ካለህ ፎቶውን ትልካለህ፣ ከሌለህ ዝም ብሎ ጽሁፉን መላክ ይቻላል
            try:
                bot.send_photo(message.chat.id, BANNER_IMG, caption=caption, parse_mode="HTML", reply_markup=markup)
            except:
                bot.send_message(message.chat.id, caption, parse_mode="HTML", reply_markup=markup)

    except Exception as e:
        print(e)

# --- START ---
if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    
    print("✅ Webhook Set & Server Starting...")
    
    from waitress import serve
    port = int(os.environ.get('PORT', 8080))
    serve(app, host="0.0.0.0", port=port)
