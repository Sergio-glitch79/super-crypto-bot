from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = "7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg"

app = Flask(__name__)
bot = Bot(token=TOKEN)

# Диспетчер и обработчики
dispatcher = Dispatcher(bot, None, workers=1)

def start(update, context):
    update.message.reply_text("👋 Привет! Я Crypto Signal Advisor. Введи /help, чтобы увидеть команды.")

def help_command(update, context):
    update.message.reply_text("📋 Команды:\n/start — Запуск бота\n/help — Помощь")

def unknown(update, context):
    update.message.reply_text("🤖 Я не понимаю эту команду. Введите /help.")

# Регистрируем обработчики
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # все неизвестные команды

@app.route('/')
def index():
    return '✅ Bot is live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
