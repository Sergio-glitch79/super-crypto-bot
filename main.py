import os
from telegram.ext import Updater
from dotenv import load_dotenv
from bot.handlers import register_handlers

def main():
    load_dotenv()
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("❌ Не указан TELEGRAM_BOT_TOKEN в переменных окружения.")

    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    register_handlers(dp)

    print("✅ Бот запущен.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
