import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import openai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)

openai.api_key = OPENAI_API_KEY

# Команда /start
def start(update, context):
    chat_id = update.effective_chat.id
    print(f"🔎 CHAT_ID = {chat_id}")
    context.bot.send_message(chat_id=chat_id, text="👋 Привет! Я бот с AI. Напиши мне что-нибудь.")

# Обработка любого текста
def handle_message(update, context):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message["content"]
    context.bot.send_message(chat_id=chat_id, text=reply)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook маршрут
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Установка webhook при запуске
@app.route('/')
def index():
    webhook_url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TELEGRAM_TOKEN}"
    bot.set_webhook(url=webhook_url)
    return "Webhook установлен!"

if __name__ == "__main__":
    app.run(port=10000, host="0.0.0.0")
