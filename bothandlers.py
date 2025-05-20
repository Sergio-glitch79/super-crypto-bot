from telegram.ext import CommandHandler

def start(update, context):
    update.message.reply_text("🚀 Привет! Я супер крипто-бот. Готов к бою!")

def help_command(update, context):
    update.message.reply_text("🆘 Доступные команды:\n/start — запуск\n/help — помощь")

def register_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
