from flask import Flask, request
from telegram import Bot, Update, InputFile
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext
import os
import zipfile
import rarfile

app = Flask(__name__)

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
bot = Bot(bot_token)
dispatcher = Dispatcher(bot, None, use_context=True)

@app.route('/telegram', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Ciao! Sono il tuo bot. Per favore, invia o carica un file .zip o .rar.')

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def handle_document(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    filename = file.file_path.split("/")[-1]
    file.download(filename)
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall('.')
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                context.bot.send_document(chat_id=update.message.from_user.id, document=InputFile(f))

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
document_handler = MessageHandler(Filters.document, handle_document)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(document_handler)

if __name__ == '__main__':
    app.run(port=8000)
