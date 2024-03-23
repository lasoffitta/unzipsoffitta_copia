from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Koyeb'

@app.route('/telegram', methods=['POST'])
def handle_telegram_webhook():
    data = json.loads(request.data)  # Carica i dati del messaggio
    # Gestisci il messaggio qui
    return 'ok'

if __name__ == "__main__":
    app.run()
