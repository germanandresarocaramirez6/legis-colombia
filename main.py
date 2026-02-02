import os
import telebot
from telebot import types
from flask import Flask
from threading import Thread

# --- CONFIGURACIÓN DEL SERVIDOR WEB ---
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot de Blindaje Legal en línea ✅"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# --- CONFIGURACIÓN DEL BOT ---
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def bienvenida(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_salud = types.InlineKeyboardButton("🏥 RECLAMO SALUD", callback_data="salud")
    btn_servicios = types.InlineKeyboardButton("💧 SERVICIOS PÚBLICOS", callback_data="servicios")
    markup.add(btn_salud, btn_servicios)
    
    bot.send_message(message.chat.id, "⚖️ **BIENVENIDO A BLINDAJE LEGAL COLOMBIA**\n\n¿En qué área necesitas asesoría hoy?", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def responder(call):
    if call.data == "salud":
        bot.edit_message_text("Has seleccionado **SALUD**. Pronto un asesor te contactará.", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
    elif call.data == "servicios":
        bot.edit_message_text("Has seleccionado **SERVICIOS PÚBLICOS**. Por favor indica tu ciudad.", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    # Iniciar servidor web en un hilo aparte
    t = Thread(target=run)
    t.start()
    # Iniciar el bot
    print("Bot encendido exitosamente...")
    bot.infinity_polling()
    
