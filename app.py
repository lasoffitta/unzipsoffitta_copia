import os
from telethon import TelegramClient, events

api_id = os.environ['TELEGRAM_API_ID']
api_hash = os.environ['TELEGRAM_API_HASH']
bot_token = os.environ['TELEGRAM_BOT_TOKEN']

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('Ciao! Sono il tuo bot. Per favore, invia o carica un file .zip o .rar.')
    raise events.StopPropagation

@bot.on(events.NewMessage)
async def echo(event):
    await event.respond(event.text)

def main():
    bot.run_until_disconnected()

if __name__ == '__main__':
    main()
