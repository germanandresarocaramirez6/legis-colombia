import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB (Truco para 24/7) ---
app = Flask('')
@app.route('/')
def home(): return "Bot Activo 🚀"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- CONFIGURACIÓN BOT ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def bienvenida(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_salud = types.InlineKeyboardButton("🏥 RECLAMO SALUD (Ley 1751)", callback_data="salud")
    btn_servicios = types.InlineKeyboardButton("📱 SERVICIOS PÚBLICOS (Ley 142)", callback_data="servicios")
    markup.add(btn_salud, btn_servicios)
    bot.send_message(message.chat.id, "⚖️ **LEGISCOLOMBIA**\nSelecciona tu trámite:", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def responder(call):
    if call.data == "salud":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🩺 **MODO SALUD**\n¿Qué te niegan?")
    elif call.data == "servicios":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📡 **MODO SERVICIOS**\n¿Qué empresa es?")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
  
