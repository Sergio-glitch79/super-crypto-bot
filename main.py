import os
from flask import Flask, request
import requests

app = Flask(__name__)

# Берём токен из переменных окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN не задан в окружении")

# Базовый URL для запросов к Telegram API
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Корневой маршрут — для проверки доступности сервиса
@app.route("/", methods=["GET"])
def index():
    return "Бот жив и работает! ✅", 200

# Маршрут для Webhook — Telegram будет POST-ить сюда обновления
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    # Если пришло сообщение
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # Обработка команд
        if text == "/start":
            reply = "✅ Супербот запущен! Я готов к бою!"
        elif text == "/help":
            reply = "ℹ️ Доступные команды:\n/start — запуск\n/help — помощь"
        else:
            reply = f"Вы написали: {text}"

        # Отправляем ответ
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )
    return {"ok": True}, 200

if __name__ == "__main__":
    # Render передаёт порт в переменную PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
