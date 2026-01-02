import telebot
import requests
import urllib.parse
import os
import threading
from flask import Flask
from telebot.types import WebAppInfo, MenuButtonWebApp, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# ⚙️ CONFIGURATION
TOKEN = '8570666490:AAHkzva23guJaWJRn2bUoV2ahI54T9PAtGs'
DOMAIN = 'https://royalspin.wuaze.com'
CHANNEL_LINK = 'https://t.me/afro_game'
SUPPORT_USER = 'https://t.me/afro_game'
BANNER_IMG = "https://gemini.google.com/share/f4cb937673b2"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- WEB SERVER TO KEEP BOT ALIVE ---
@app.route('/')
def home():
    return "Bot is running!"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def get_play_link(user_id, name, phone):
    safe_name = urllib.parse.quote(name) if name else "Player"
    safe_phone = phone if phone else "0000"
    return f"{DOMAIN}/index.php?tg_id={user_id}&name={safe_name}&phone={safe_phone}"

# --- HANDLERS ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        user_id = message.from_user.id
        first_name = message.from_user.first_name if message.from_user.first_name else "Friend"
        chat_id = message.chat.id
        
        # Check user status (Optional: Assuming new for simplicity or adding check logic here)
        show_main_menu(chat_id, user_id, first_name)
            
    except Exception as e:
        print(f"Error: {e}")

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    try:
        user_id = message.contact.user_id
        first_name = message.contact.first_name
        phone = message.contact.phone_number
        
        clean_phone = phone.replace('+', '').replace(' ', '')
        if clean_phone.startswith('251'): clean_phone = '0' + clean_phone[3:]
        
        bot.send_message(message.chat.id, "✅ ተቀባይነት አግኝቷል!", reply_markup=ReplyKeyboardRemove())
        show_main_menu(message.chat.id, user_id, first_name, clean_phone)
    except: pass

def show_main_menu(chat_id, user_id, name, phone="0000"):
    game_url = get_play_link(user_id, name, phone)
    wallet_url = f"{DOMAIN}/wallet.php"

    try:
        bot.set_chat_menu_button(
            chat_id=chat_id,
            menu_button=MenuButtonWebApp(type="web_app", text="PLAY NOW 🚀", web_app=WebAppInfo(url=game_url))
        )
    except: pass

    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("🚀 PLAY NOW 🚀", web_app=WebAppInfo(url=game_url)))
    markup.row(InlineKeyboardButton("💰 Deposit", web_app=WebAppInfo(url=wallet_url)), InlineKeyboardButton("📢 Channel", url=CHANNEL_LINK))
    markup.row(InlineKeyboardButton("💬 Support", url=SUPPORT_USER))

    msg = f"👋 <b>Hello {name}!</b>\n\nWelcome to <b>AFRO GAMES</b>!\nPlay and Win Big! 🏆\n\n👇 <b>Click below to start playing!</b>"
    
    try:
        bot.send_photo(chat_id, BANNER_IMG, caption=msg, parse_mode="HTML", reply_markup=markup)
    except:
        bot.send_message(chat_id, msg, parse_mode="HTML", reply_markup=markup)

# --- START ---
if __name__ == "__main__":
    # Start Web Server in Background
    t = threading.Thread(target=run_web)
    t.start()
    
    # Start Bot
    print("🤖 Bot Started...")
    bot.infinity_polling()