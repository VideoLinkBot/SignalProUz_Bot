import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Tokenni Render Environment Variables dan olish
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Asosiy menyu tugmalari
main_menu = ReplyKeyboardMarkup(
    [["💵 Valyuta kurslari", "🥇 Oltin kursi"],
     ["📊 Signal olish"]],
    resize_keyboard=True
)

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

# Valyuta kurslari
async def valyuta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        data = requests.get(url, timeout=10).json()

        kurslar = {
            "USD": "🇺🇸 Dollar",
            "EUR": "🇪🇺 Yevro",
            "RUB": "🇷🇺 Rubl",
            "GBP": "🇬🇧 Funt",
            "CNY": "🇨🇳 Yuan",
            "JPY": "🇯🇵 Yen",
            "KZT": "🇰🇿 Tenge",
            "KGS": "🇰🇬 Som",
            "TRY": "🇹🇷 Lira",
            "AED": "🇦🇪 Dirham",
            "SAR": "🇸🇦 Riyal",
            "INR": "🇮🇳 Rupiya",
            "SGD": "🇸🇬 Singapur dollari",
            "KRW": "🇰🇷 Von",
            "CHF": "🇨🇭 Frank"
        }

        msg = "💱 *Valyuta kurslari:*\n\n"
        for code, name in kurslar.items():
            item = next((i for i in data if i["Ccy"] == code), None)
            if item:
                msg += f"{name} = {item['Rate']} so‘m\n"

        await update.message.reply_text(msg, parse_mode="Markdown")
    except Exception:
        await update.message.reply_text("❌ Kurslarni olishda xatolik. Keyinroq urinib ko‘ring.")

# Oltin kursi (ishlaydigan va xatoliklarni oldini oladi)
async def oltin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Oltin kursini qidirish
        xau = next((item for item in data if item.get("Ccy") == "XAU"), None)

        if xau:
            msg = (
                f"🥇 *Oltin kursi* ({xau['Date']}):\n\n"
                f"1 gramm oltin = {xau['Rate']} so‘m"
            )
        else:
            msg = "❌ Bugun oltin kursi mavjud emas."

        await update.message.reply_text(msg, parse_mode="Markdown")

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"❌ Kursni olishda xatolik:\n{e}")
    except Exception as e:
        await update.message.reply_text(f"❌ Kutilmagan xatolik:\n{e}")

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

    # Tugmalar uchun MessageHandler
    app.add_handler(MessageHandler(filters.Text("💵 Valyuta kurslari"), valyuta))
    app.add_handler(MessageHandler(filters.Text("🥇 Oltin kursi"), oltin))
    app.add_handler(MessageHandler(filters.Text("📊 Signal olish"), signal))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
