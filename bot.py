from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import MessageEntity
import logging
import os

# Log sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.environ.get("TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

# Xabar ID va foydalanuvchi ID ni vaqtincha saqlash uchun
user_message_map = {}

def start(update, context):
    update.message.reply_text("Salom! Menga 'humo' yoki 'uzcard' deb yozing.")

def handle_text(update, context):
    user_id = update.message.chat_id
    text = update.message.text.lower()

    if text == "humo":
        update.message.reply_text("9860170103586914")
    elif text == "uzcard":
        update.message.reply_text("5614681915173910")
    else:
        # Foydalanuvchi xabarini adminga forward qiladi va mapping saqlaydi
        forwarded = context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=user_id, message_id=update.message.message_id)
        user_message_map[forwarded.message_id] = user_id

def handle_photo(update, context):
    forwarded = context.bot.forward_message(chat_id=ADMIN_ID, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
    user_message_map[forwarded.message_id] = update.message.chat_id

def reply_handler(update, context):
    if update.message.reply_to_message:
        reply_msg_id = update.message.reply_to_message.message_id

        if reply_msg_id in user_message_map:
            target_user_id = user_message_map[reply_msg_id]
            context.bot.send_message(chat_id=target_user_id, text=update.message.text)
            update.message.reply_text("✅ Javob yuborildi")
        else:
            update.message.reply_text("⚠️ Bu reply kimga tegishli ekanligini aniqlay olmadim.")
    else:
        update.message.reply_text("❗ Iltimos, reply orqali yozing.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & Filters.chat(chat_id=ADMIN_ID), reply_handler))  # Admin reply
    dp.add_handler(MessageHandler(Filters.text & ~Filters.chat(chat_id=ADMIN_ID), handle_text))   # User matn
    dp.add_handler(MessageHandler(Filters.photo & ~Filters.chat(chat_id=ADMIN_ID), handle_photo)) # User rasm

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
