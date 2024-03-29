from flask import Flask, request
from telegram import Bot, Update, InputFile
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext
import os
import tempfile
import zipfile
from PyPDF2 import PdfFileReader
from pdf2image import convert_from_path

app = Flask(__name__)

bot_token = os.environ['TELEGRAM_BOT_TOKEN']
bot = Bot(bot_token)
dispatcher = Dispatcher(bot, None, use_context=True)

@app.route('/telegram', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route('/')
def index():
    return "Hello, World!"

def get_pdf_images(pdf_path, output_folder):
    images = convert_from_path(pdf_path)
    image_paths = []
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i+1}.jpg")
        image.save(image_path, "JPEG")
        image_paths.append(image_path)
    return image_paths

def create_cbz_from_images(image_paths, output_path):
    with zipfile.ZipFile(output_path, 'w') as cbz_file:
        for image_path in image_paths:
            cbz_file.write(image_path, os.path.basename(image_path))

def handle_document(update: Update, context: CallbackContext) -> None:
    file = context.bot.getFile(update.message.document.file_id)
    filename = file.file_path.split("/")[-1]
    file.download(filename)
    
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extract images from the PDF file
        image_paths = get_pdf_images(filename, temp_dir)
        # Create CBZ file from the extracted images
        cbz_path = os.path.join(temp_dir, os.path.splitext(filename)[0] + ".cbz")
        create_cbz_from_images(image_paths, cbz_path)
        
        # Send the CBZ file back to the user
        with open(cbz_path, 'rb') as cbz_file:
            context.bot.send_document(chat_id=update.message.chat_id, document=InputFile(cbz_file))
    
start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
document_handler = MessageHandler(Filters.document, handle_document)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(document_handler)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
