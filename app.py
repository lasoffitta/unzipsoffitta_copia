from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import json
import requests
import os
import zipfile

app = Flask(__name__)

TOKEN = '6925431313:AAHsfhZ9tsGbYhykiOn400djYBpePo-pr6Q'  # Sostituisci con il tuo token di Telegram
bot = Bot(TOKEN)
updater = Updater(token=TOKEN, use_context=True)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Benvenuto! Inviami un file .zip o .rar.")

def handle_document(update, context):
    file = context.bot.getFile(update.message.document.file_id)
    file.download(update.message.document.file_name)

    keyboard = [[InlineKeyboardButton("Sì", callback_data='extract')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Vuoi estrarre il file?', reply_markup=reply_markup)

def handle_callback_query(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'extract':
        file_name = query.message.reply_to_message.document.file_name
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall()

            query.edit_message_text(text="File estratto con successo.")

start_handler = CommandHandler('start', start)
document_handler = MessageHandler(Filters.document, handle_document)
callback_query_handler = CallbackQueryHandler(handle_callback_query)

updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(document_handler)
updater.dispatcher.add_handler(callback_query_handler)

@app.route('/telegram', methods=['POST'])
def handle_telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    updater.dispatcher.process_update(update)
    return 'ok'

if __name__ == "__main__":
    updater.start_polling()
    app.run()
