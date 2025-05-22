from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = "7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg"

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route('/')
def index():
    return '🚀 Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# Обработчики команд
def start(update, context):
    update.message.reply_text("👋 Привет! Я твой Crypto Signal Advisor. Введи /help, чтобы узнать команды.")

def help_command(update, context):
    update.message.reply_text("📋 Доступные команды:\n/start - запуск бота\n/help - список команд")

def unknown(update, context):
    update.message.reply_text("🤖 Я не понимаю эту команду. Введите /help.")

# Настройка диспетчера
from telegram.ext import Dispatcher
dispatcher = Dispatcher(bot, None, workers=0)
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler(None, unknown))  # обработка неизвестных

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
