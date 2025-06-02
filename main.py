import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from openai import OpenAI

# Загрузка .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Flask и Telegram
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot, None, workers=1, use_context=True)
client = OpenAI(api_key=OPENAI_API_KEY)

# /start команда
def start(update, context):
    chat_id = update.effective_chat.id
    print(f"💬 CHAT_ID: {chat_id}")
    context.bot.send_message(chat_id=chat_id, text="Привет! Я готов отвечать на твои вопросы с помощью OpenAI!")

# Обработка обычных сообщений
def handle_message(update, context):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = f"Ошибка от OpenAI: {e}"

    context.bot.send_message(chat_id=chat_id, text=reply)

# Регистрация хендлеров
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Webhook маршрут
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

# Установка Webhook
@app.route("/")
def index():
    url = f"https://{os.environ['RENDER_EXTERNAL_HOSTNAME']}/{TELEGRAM_TOKEN}"
    bot.set_webhook(url=url)
    return "Webhook установлен!"

# Запуск Flask
if __name__ == "__main__":
    app.run(port=10000, host="0.0.0.0")
