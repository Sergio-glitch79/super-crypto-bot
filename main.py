from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os
import ccxt
import threading
import time
import openai

# Токен Telegram бота
TOKEN = '7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg'
bot = Bot(token=TOKEN)

# Flask приложение
app = Flask(__name__)

# Получение сигнала по всем парам

def get_top_signals():
    try:
        exchange = ccxt.bingx()
        markets = exchange.load_markets()
        signals = []

        for symbol in markets:
            if "/USDT" in symbol:
                try:
                    ticker = exchange.fetch_ticker(symbol)
                    change = ticker['percentage']
                    if change and abs(change) > 3:
                        signals.append(f"🚀 {symbol}: {ticker['last']} USDT ({change:+.2f}%)")
                except:
                    continue

        return "\n".join(signals) if signals else "ℹ️ Нет сильных движений сейчас."
    except Exception as e:
        return f"❌ Ошибка получения данных: {str(e)}"

# Автоматическая отправка сигналов каждые 10 минут

def auto_signal():
    chat_id = os.environ.get("CHAT_ID")
    if not chat_id:
        print("❗ Укажите CHAT_ID для авторассылки")
        return
    while True:
        try:
            signal = get_top_signals()
            bot.send_message(chat_id=chat_id, text=signal)
            time.sleep(600)  # каждые 10 минут
        except Exception as e:
            print(f"Ошибка авторассылки: {e}")
            time.sleep(60)

# Команда /start

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="👋 Привет! Я Crypto Signal Advisor. Сигналы по сильным движениям криптовалют приходят каждые 10 минут. Введи /help для помощи.")
print(f"🔎 CHAT_ID = {update.effective_chat.id}")
# Команда /help

def help_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="📋 Команды:\n/start — Запуск бота\n/help — Помощь\n/signal — Получить текущие сигналы\n/ask — Задать вопрос AI")

# Команда /signal

def signal_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=get_top_signals())

# Команда /ask — AI-помощник

def ask_ai(update, context):
    user_question = " ".join(context.args)
    if not user_question:
        context.bot.send_message(chat_id=update.effective_chat.id, text="✍️ Напиши вопрос после /ask")
        return

    try:
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_question}]
        )
        reply = response['choices'][0]['message']['content']
        context.bot.send_message(chat_id=update.effective_chat.id, text=reply)
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"❌ Ошибка AI: {str(e)}")

# Обработка текста

def handle_text(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="🤖 Я не понимаю эту команду. Введите /help.")

@app.route('/')
def home():
    return 'OK'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot, None, workers=1, use_context=True)

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('signal', signal_command))
    dispatcher.add_handler(CommandHandler('ask', ask_ai))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dispatcher.add_handler(MessageHandler(Filters.command, handle_text))

    dispatcher.process_update(update)
    return 'ok'

if __name__ == '__main__':
    threading.Thread(target=auto_signal, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)

