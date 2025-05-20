from flask import Flask, request
import os
import telegram

TOKEN = "7049684701:AAFoGlDQKQBPg1Tw9Xa3p2btw5IHgCPM8Qg"
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "Супербот работает! ✅"

# Обработчик Webhook от Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def receive_update():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        bot.send_message(chat_id=chat_id, text=f"Вы написали: {text}")

    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
