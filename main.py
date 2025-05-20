import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Твой токен Telegram-бота из BotFather
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

@app.route("/", methods=["GET"])
def index():
    return "Бот жив и работает! ✅"

# Этот маршрут принимает Webhook от Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        if text == "/start":
            reply = "✅ Супербот запущен! Я готов к бою!"
        elif text == "/help":
            reply = "Доступные команды:\n/start — запуск\n/help — помощь"
        else:
            reply = f"Вы написали: {text}"

        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    return {"ok": True}

if __name__ == "__main__":
    # Render передаёт порт в переменную окружения PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
