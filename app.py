from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import os

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

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)

if __name__ == '__main__':
    app.run(port=8000)
