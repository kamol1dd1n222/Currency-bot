import requests
from telegram.ext import (
    Updater, CallbackContext,
    CommandHandler, MessageHandler, Filters
)
from telegram import Update
from config import TOKEN


def get_usd_rate() -> float:
    response = requests.get('https://cbu.uz/uz/arkhiv-kursov-valyut/json/USD/')
    data = response.json()
    kurs = float(data[0]['Rate'])
    return kurs


def start_command(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Assalomu alaykum!\n"
        "Valyuta konvertatsiya botiga xush kelibsiz. 🗳️\n\n"
        "1 - UZS → USD\n"
        "2 - USD → UZS\n\n"
        "Iltimos, kerakli raqamni yuboring."
    )
    context.user_data['step'] = "choose"   # qaysi bosqichda ekanini saqlaymiz


def handle_message(update: Update, context: CallbackContext):
    step = context.user_data.get("step")

    # 1-bosqich: yo‘nalish tanlash
    if step == "choose":
        text = update.message.text.strip()
        if text not in ["1", "2"]:
            update.message.reply_text("❌ Noto'g'ri tanlov! Faqat 1 yoki 2 yuboring.")
            return

        context.user_data['direction'] = text
        context.user_data['step'] = "amount"

        if text == "1":
            update.message.reply_text("UZS miqdorini kiriting:")
        else:
            update.message.reply_text("USD miqdorini kiriting:")

    
    elif step == "amount":
        try:
            amount = float(update.message.text.strip())
        except ValueError:
            update.message.reply_text("❌ Iltimos, faqat son yuboring.")
            return

        rate = get_usd_rate()
        tanlov = context.user_data.get('direction')

        if tanlov == "1":  
            result = amount / rate
            update.message.reply_text(f"💱 Natija: {amount:,.2f} UZS = {result:,.2f} USD")
        else:  
            result = amount * rate
            update.message.reply_text(f"💱 Natija: {amount:,.2f} USD = {result:,.2f} UZS")

        update.message.reply_text("Yana konvertatsiya qilish uchun 1 yoki 2 ni yuboring. 🔄")
        context.user_data['step'] = "choose"

    else:
        update.message.reply_text("Iltimos, /start buyrug‘ini yuboring.")


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
