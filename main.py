from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os

# Токен Telegram бота
TOKEN = '7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg'
bot = Bot(token=TOKEN)

# Flask приложение
app = Flask(__name__)

# Команда /start
def start(update, context):
    keyboard = [[InlineKeyboardButton("Получить сигнал", callback_data='get_signal')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "👋 Привет! Я Crypto Signal Advisor. Введи /help, чтобы увидеть команды.",
        reply_markup=reply_markup
    )

# Команда /help
def help_command(update, context):
    update.message.reply_text("📋 Команды:\n/start — Запуск бота\n/help — Помощь\n/signal — Получить криптосигнал")

# Команда /signal (заглушка для будущих сигналов)
def signal_command(update, context):
    update.message.reply_text("📈 Сигнал: Покупка BTC/USDT на пробое уровня 70,000. Stop Loss: 68,500. Take Profit: 73,000.")

# Обработка обычных сообщений
def handle_text(update, context):
    text = update.message.text.lower()
    if 'btc' in text or 'сигнал' in text:
        signal_command(update, context)
    else:
        update.message.reply_text("🤖 Я не понимаю эту команду. Введите /help.")

# Обработка нажатий кнопок
def button_callback(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'get_signal':
        query.edit_message_text("📈 Сигнал: LONG ETH/USDT от 3000, SL: 2900, TP: 3200")

@app.route('/')
def home():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

    # Регистрируем обработчики
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('signal', signal_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dispatcher.add_handler(MessageHandler(Filters.command, handle_text))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'.*'), handle_text))
    from telegram.ext import CallbackQueryHandler
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

