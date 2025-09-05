import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Bot tokenini Render environment variables ichidan olamiz
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! 👋 Bu SignalProUz_Bot. Tez orada sizga kurslarni yuboraman.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
