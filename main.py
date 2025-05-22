from flask import Flask, request
import telegram

app = Flask(__name__)

# Замените на свой токен
TOKEN = '7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg'
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return 'Бот работает!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    if 'message' in data:
        chat_id = data['message']['chat']['id']
        text = data['message'].get('text', '')

        if text == '/start':
            bot.send_message(chat_id=chat_id, text="👋 Привет! Я бот для сигналов.")
        elif text == '/help':
            bot.send_message(chat_id=chat_id, text="📌 Команды:\n/start — Запуск\n/help — Помощь\n/status — Статус бота")
        elif text == '/status':
            bot.send_message(chat_id=chat_id, text="✅ Бот активен и работает.")
        else:
            bot.send_message(chat_id=chat_id, text="🤖 Я не понимаю эту команду. Введите /help.")
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
