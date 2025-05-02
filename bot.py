from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

# Log format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# TOKEN va ADMIN ID (Render uchun environmentdan olinadi)
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

# /start buyrug‘iga javob
def start(update, context):
    update.message.reply_text("Salom! Menga 'humo' yoki 'uzcard' deb yozing.")

# Matnli xabarlarni qayta ishlash
def handle_text(update, context):
    user_id = update.message.chat_id
    text = update.message.text.lower()

    if text == "humo":
        update.message.reply_text("9860170103586914")
    elif text == "uzcard":
        update.message.reply_text("5614681915173910")
    else:
        # Boshqa xabarni adminga forward qiladi
        context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=update.message.message_id)

# Rasm, foto va boshqa fayllarni forward qilish
def handle_photo(update, context):
    context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)

# Admin foydalanuvchiga /reply orqali javob yozishi
def reply_to_user(update, context):
    try:
        args = context.args
        user_id = int(args[0])
        message = " ".join(args[1:])
        context.bot.send_message(chat_id=user_id, text=message)
        update.message.reply_text("✅ Yuborildi")
    except Exception as e:
        update.message.reply_text(f"Xatolik: {e}")

# Bot ishga tushadigan asosiy funksiya
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reply", reply_to_user))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_text))
    dp.add_handler(MessageHandler(Filters.photo, handle_photo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
