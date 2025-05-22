from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = '7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg'
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Супербот работает!'

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

def start(update, context):
    update.message.reply_text('Привет! Я супербот!')

# Подключаем диспетчер
dispatcher = Dispatcher(bot, None, use_context=True)
dispatcher.add_handler(CommandHandler('start', start))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
