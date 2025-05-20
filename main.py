from telegram.ext import Updater
from bot.handlers import register_handlers
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    register_handlers(dispatcher)

    print("Привет! Я супербот для крипты. Готов к работе!")

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
