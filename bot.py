from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import os
from datetime import datetime
import pytz

# Log sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

# Ish vaqtini tekshiruvchi funksiya
def is_within_working_hours():
    uzbekistan = pytz.timezone("Asia/Tashkent")
    now = datetime.now(uzbekistan)
    start_hour = 9
    end_hour = 23
    return start_hour <= now.hour < end_hour

# Foydalanuvchi ID ni vaqtincha saqlash uchun
user_message_map = {}

# /start buyrug‘i
def start(update, context):
    keyboard = [
        [InlineKeyboardButton("💳 Visa", callback_data='visa')],
        [InlineKeyboardButton("💳 Uzcard", callback_data='uzcard')],
        [InlineKeyboardButton("💳 Humo", callback_data='humo')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Quyidagilardan birini tanlang:", reply_markup=reply_markup)

# Tugma bosilganda
def button_handler(update, context):
    query = update.callback_query
    query.answer()
    card = query.data

    cards = {
        "visa": "4790912210044568",
        "uzcard": "5614681915173910",
        "humo": "9860170103586914"
    }

    query.edit_message_text(text=f"{card.upper()} raqam: {cards[card]}")

# Matnli xabarlar
def handle_text(update, context):
    if not is_within_working_hours():
        update.message.reply_text("🕒 Hozir ish vaqtidan tashqarida. Iltimos, 09:00–23:00 oralig‘ida yozing.")
        return

    text = update.message.text.lower()

    if text == "humo":
        update.message.reply_text("9860170103586914")
    elif text == "uzcard":
        update.message.reply_text("5614681915173910")
    elif text == "visa":
        update.message.reply_text("4790912210044568")
    else:
        update.message.reply_text("❗ Iltimos, faqat quyidagilardan birini yozing: 'humo', 'uzcard', 'visa'")
        forwarded = context.bot.forward_message(
            chat_id=ADMIN_ID,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        user_message_map[forwarded.message_id] = update.message.chat_id

# Surat yuborilganda
def handle_photo(update, context):
    update.message.reply_text("🖼 Surat qabul qilindi ✅")
    context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

# Fayl yuborilganda
def handle_document(update, context):
    update.message.reply_text("📎 Fayl qabul qilindi ✅")
    context.bot.forward_message(
        chat_id=ADMIN_ID,
        from_chat_id=update.message.chat_id,
        message_id=update.message.message_id
    )

# Botni ishga tushirish
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))
    dp.add_handler(MessageHandler(Filters.document, handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

