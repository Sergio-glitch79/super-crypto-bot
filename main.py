import telebot
import os
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Привет! Я супербот. Скоро буду присылать сигналы 📈")

def main():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print("Ошибка:", e)
            time.sleep(5)

if __name__ == '__main__':
    main()
