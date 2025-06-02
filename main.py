import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Загрузка переменных окружения
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Установка ключа OpenAI
openai.api_key = OPENAI_API_KEY

# Команда /start
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Привет! Я бот с ИИ. Напиши мне что-нибудь.")

# Обработка всех сообщений
def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    chat_id = update.effective_chat.id

    # Запрос к OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = f"Произошла ошибка при запросе к OpenAI: {e}"

    update.message.reply_text(f"💡 AI: {answer}")
    print(f"🔎 CHAT_ID = {chat_id}")

# Запуск бота
def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("✅ Бот запущен")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
