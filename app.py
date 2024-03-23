from flask import Flask, request
import json
import requests
import os
import zipfile

app = Flask(__name__)

TOKEN = '6925431313:AAHsfhZ9tsGbYhykiOn400djYBpePo-pr6Q'  # Sostituisci con il tuo token di Telegram

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

@app.route('/telegram', methods=['POST'])
def handle_telegram_webhook():
    data = json.loads(request.data)  # Carica i dati del messaggio

    # Controlla se il messaggio è un comando /start
    if 'text' in data['message'] and data['message']['text'] == '/start':
        chat_id = data['message']['chat']['id']
        requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text=Benvenuto! Inviami un file .zip o .rar.')

    # Controlla se il messaggio contiene un documento
    elif 'document' in data['message']:
        file_id = data['message']['document']['file_id']
        file_name = data['message']['document']['file_name']

        # Scarica il file
        file_path = requests.get(f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}').json()['result']['file_path']
        file = requests.get(f'https://api.telegram.org/file/bot{TOKEN}/{file_path}')
        open(file_name, 'wb').write(file.content)

        # Estrai il file se è un .zip
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                zip_ref.extractall()

            # Invia un messaggio di conferma
            chat_id = data['message']['chat']['id']
            requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text=File%20estratto%20con%20successo.')

    return 'ok'

if __name__ == "__main__":
    app.run()
