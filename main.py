import telebot
import os
import time
import urllib.parse
from flask import Flask, request
from telebot.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from waitress import serve

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
TOKEN = '8570666490:AAH08os9NH0oBwYPFaZ49kVEY6e56lTn7hk' 
DOMAIN = 'https://afrogames.et' 
CHANNEL_LINK = 'https://t.me/afro_game'
SUPPORT_USER = 'https://t.me/afro_game'

# ማሳሰቢያ፡ ይህ የ Gemini ሊንክ ቴሌግራም ላይ እንደ ፎቶ አይሰራም። 
# በትክክል እንዲታይ ቀጥታ የፎቶ ሊንክ (ለምሳሌ .jpg የሚያልቅ) ወይም የቴሌግራም file_id መጠቀም አለብህ።
BANNER_IMG = "https://gemini.google.com/share/508fab1dec30" 

WEBHOOK_URL_BASE = "https://afro-bot.onrender.com" 
WEBHOOK_URL_PATH = f"/{TOKEN}/"

# threaded=True ቦቱ በአንድ ጊዜ ብዙ ስራ እንዲሰራ ያደርገዋል (ፈጣን ነው)
bot = telebot.TeleBot(TOKEN, threaded=True)
app = Flask(__name__)

# --- WEB SERVER ---
@app.route('/', methods=['GET'])
def index():
    return "🔥 AFRO GAMES BOT IS RUNNING! 🔥", 200

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    return 'Forbidden', 403

# --- HELPER FUNCTIONS ---
def get_game_url(user_id, name, phone):
    safe_name = urllib.parse.quote(str(name))
    return f"{DOMAIN}/index.php?tg_id={user_id}&name={safe_name}&phone={phone}"

def get_wallet_url(user_id):
    return f"{DOMAIN}/wallet.php?tg_id={user_id}"

# ==========================================
# 🔥 HANDLERS (አዲሱ የማስታወቂያ ፅሁፍ የገባበት)
# ==========================================

@bot.message_handler(commands=['start'])
def send_welcome(message):
    first_name = message.from_user.first_name if message.from_user.first_name else "ወዳጄ"
    
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_btn = KeyboardButton(text="📱 ለመመዝገብ ይህን ይጫኑ (Register)", request_contact=True)
    markup.add(phone_btn)

    msg = (
        f"👋 <b>ሰላም {first_name}! እንኳን ወደ AFRO GAMES በደህና መጡ!</b> 🇪🇹\n\n"
        f"እዚህ የብዙዎች ተወዳጅ በሆኑት ጨዋታዎች ዘና እያሉ የዕለቱ ትልቅ አሸናፊ ይሆናሉ!\n\n"
        f"🎯 <b>ምን መጫወት ይፈልጋሉ?</b>\n"
        f"በቦታችን ላይ <b>ቢንጎ (Bingo)፣ ክራሽ (Crash 🚀)፣ ማይን (Mine 💣) እና ኬኖ (Keno 🎱)</b> ይጠብቁዎታል።\n\n"
        f"🎁 <b>ለመጀመር አካውንት መክፈት ያስፈልግዎታል።</b>\n"
        f"ከታች ያለውን <b>'📱 ለመመዝገብ ይህን ይጫኑ'</b> የሚለውን በተን ይንኩ። 👇"
    )
    bot.send_message(message.chat.id, msg, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if not message.contact:
        return

    user_id = message.from_user.id
    first_name = message.from_user.first_name or "Gamer"
    phone_number = message.contact.phone_number
    
    game_link = get_game_url(user_id, first_name, phone_number)
    wallet_link = get_wallet_url(user_id)

    # የግራ በኩል "Play" በተንን በፍጥነት ማቀናበር
    try:
        bot.set_chat_menu_button(
            chat_id=message.chat.id,
            menu_button=MenuButtonWebApp(type="web_app", text="🎮 PLAY NOW", web_app=WebAppInfo(url=game_link))
        )
    except: pass

    # Inline Buttons
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🎰 ወደ ጨዋታው ይግቡ (PLAY) 🎰", web_app=WebAppInfo(url=game_link)))
    markup.row(
        InlineKeyboardButton("💰 ሂሳብ (Wallet)", web_app=WebAppInfo(url=wallet_link)), 
        InlineKeyboardButton("📢 ቻናል (Join)", url=CHANNEL_LINK)
    )
    markup.row(InlineKeyboardButton("💬 እርዳታ (Support)", url=SUPPORT_USER))

    bot.send_message(message.chat.id, "✅ ምዝገባዎ ተሳክቷል!", reply_markup=telebot.types.ReplyKeyboardRemove())

    caption = (
        f"🎉 <b>እንኳን ደስ አለዎት {first_name}!</b>\n\n"
        f"✅ አካውንትዎ በተሳካ ሁኔታ ተከፍቷል! (እንደ አዲስ ተመዝጋቢ <b>ነጻ 30 ብር ቦነስ</b> ተሰጥቶዎታል! 🎁)\n\n"
        f"💡 <b>እንዴት መጫወት ይቻላል?</b>\n"
        f"<b>1. ዲፖዚት (Deposit):</b> በ<b>ቴሌብር (Telebirr)</b> የፈለጉትን የብር መጠን በሰከንዶች ውስጥ ያስገቡ።\n"
        f"<b>2. ይጫወቱ:</b> ከሚወዱት ጨዋታ ውስጥ አንዱን መርጠው መጫወት ይጀምሩ።\n"
        f"<b>3. አየር በአየር ያውጡ:</b> ያሸነፉትን ብር ወዲያውኑ ወደ ቴሌብርዎ ያስተላልፉ (100% አስተማማኝ!)\n\n"
        f"👇 <b>'🎰 ወደ ጨዋታው ይግቡ (PLAY)'</b> የሚለውን በመጫን አሁኑኑ መጫወት ይጀምሩ! መልካም እድል! 🍀"
    )
    
    # ፎቶው ባይጫን እንኳን መልዕክቱ እንዲሄድ የተደረገ ጥንቃቄ
    try:
        bot.send_photo(message.chat.id, BANNER_IMG, caption=caption, parse_mode="HTML", reply_markup=markup)
    except:
        bot.send_message(message.chat.id, caption, parse_mode="HTML", reply_markup=markup)

# --- START ---
if __name__ == "__main__":
    # Webhook ማስተካከያ
    bot.remove_webhook()
    time.sleep(0.5)
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
    
    print(f"🚀 Bot is live on {WEBHOOK_URL_BASE}")
    port = int(os.environ.get('PORT', 8080))
    serve(app, host="0.0.0.0", port=port)
