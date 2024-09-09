from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext
import telegram.ext.filters as filters
import requests
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Scan QR Code", callback_data='scan')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Welcome! Please choose:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'scan':
        query.edit_message_text(text="Please send a photo of the QR code.")

def scan_qr(update: Update, context: CallbackContext) -> None:
    photo = update.message.photo[-1].get_file()
    photo.download('qr_code.png')

    img = cv2.imread('qr_code.png')
    decoded_objects = decode(img)
    if decoded_objects:
        qr_data = decoded_objects[0].data.decode('utf-8')
        update.message.reply_text(f'QR Code Data: {qr_data}')
        # Send data to backend
        requests.post('http://localhost:5000/scan', json={'data': qr_data})
    else:
        update.message.reply_text('No QR code found.')

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.photo, scan_qr))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
