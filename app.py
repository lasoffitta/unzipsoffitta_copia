import os
from flask import Flask, request
from telethon import TelegramClient, events
from telegram import Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater

app = Flask(__name__)

api_id = os.environ['TELEGRAM_API_ID']
api_hash = os.environ['TELEGRAM_API_HASH']
bot_token = os.environ['TELEGRAM_BOT_TOKEN']

telethon_bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
telegram_bot = Bot(bot_token)

updater = Updater(bot=telegram_bot, use_context=True)

@app.route('/')
def home():
    return "Hello, World!"

@telethon_bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Ciao! Sono il tuo bot. Per favore, invia o carica un file .zip o .rar.')
    raise events.StopPropagation

@telethon_bot.on(events.NewMessage)
async def echo(event):
    await event.respond(event.text)

def main():
    telethon_bot.start()
    app.run()
    telethon_bot.run_until_disconnected()

if __name__ == '__main__':
    main()
