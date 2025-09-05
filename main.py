import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Tokenni Render Environment Variables dan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    [["💵 Valyuta kurslari", "🥇 Oltin kursi"],
     ["📊 Signal olish"]],
    resize_keyboard=True
)

# Bayroqlar lug‘ati
flags = {
    "USD": "🇺🇸", "EUR": "🇪🇺", "RUB": "🇷🇺", "KZT": "🇰🇿", "TRY": "🇹🇷",
    "AED": "🇦🇪", "CNY": "🇨🇳", "KRW": "🇰🇷", "JPY": "🇯🇵", "GBP": "🇬🇧",
    "CHF": "🇨🇭", "SEK": "🇸🇪", "NOK": "🇳🇴", "DKK": "🇩🇰", "PLN": "🇵🇱"
}

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalomu alaykum!\n\n"
        "📌 Siz hozir *SignalProUz_Bot*dasiz.\n\n"
        "Bu yerda siz:\n"
        "💵 Valyuta kurslari\n"
        "🥇 Oltin kursi\n"
        "📊 Kunlik signallarni olishingiz mumkin.\n\n"
        "👇 Quyidagi menyudan keraklisini tanlang:",
        reply_markup=main_menu,
        parse_mode="Markdown"
    )

# Valyuta kurslari (15 ta asosiy)
async def valyuta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        data = requests.get(url).json()

        kerakli = list(flags.keys())

        msg = "💵 *Bugungi valyuta kurslari:*\n\n"
        for val in data:
            if val["Ccy"] in kerakli:
                flag = flags.get(val["Ccy"], "")
                msg += f"{flag} {val['CcyNm_UZ']} ({val['Ccy']}): {val['Rate']} so‘m\n"

        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Kurslarni olishda xatolik. Keyinroq urinib ko‘ring.")

# Oltin kursi
async def oltin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        data = requests.get(url).json()

        xau = next(item for item in data if item["Ccy"] == "XAU")
        msg = (
            f"🥇 *Oltin kursi* ({xau['Date']}):\n\n"
            f"1 gramm oltin = {xau['Rate']} so‘m"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Oltin kursini olishda xatolik.")

# Signal yuborish
async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📊 *Bugungi signal:*\n\n"
        "✅ BTC/USDT – BUY 25,300\n"
        "🎯 TP: 25,800\n"
        "🛑 SL: 24,900",
        parse_mode="Markdown"
    )

def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN topilmadi! Render Environment Variables ichida qo‘shing.")

    app = Application.builder().token(BOT_TOKEN).build()

    # Komandalar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("valyuta", valyuta))
    app.add_handler(CommandHandler("oltin", oltin))
    app.add_handler(CommandHandler("signal", signal))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
