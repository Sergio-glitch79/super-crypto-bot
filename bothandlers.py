from telegram.ext import CommandHandler

def start(update, context):
    update.message.reply_text("✅ Супербот запущен! Я готов к бою!")

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
