from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = "7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg"
bot = Bot(token=TOKEN)
app = Flask(__name__)

dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

# Команды
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Привет! Я Crypto Signal Advisor. Введи /help, чтобы увидеть команды.")

def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="📋 Команды:\n/start — Запуск бота\n/help — Помощь\n/signal — Пример сигнала\n/subscribe — Подписка\n/unsubscribe — Отписка\n/status — Статус подписки")

def signal(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="📈 Сигнал: Купить BTC по 65000, цель: 70000, стоп: 63000")

def subscribe(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Вы подписались на сигналы.")

def unsubscribe(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🚫 Вы отписались от сигналов.")

def status(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="📊 Вы подписаны на сигналы.")

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Я не понимаю эту команду. Введите /help.")

# Обработчики команд
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("signal", signal))
dispatcher.add_handler(CommandHandler("subscribe", subscribe))
dispatcher.add_handler(CommandHandler("unsubscribe", unsubscribe))
dispatcher.add_handler(CommandHandler("status", status))
dispatcher.add_handler(CommandHandler(None, unknown))  # Для неизвестных

# Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

# Корневая страница
@app.route('/', methods=['GET'])
def index():
    return "✅ Bot is running."

if __name__ == '__main__':
    app.run(debug=False)
