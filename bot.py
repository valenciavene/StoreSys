import nest_asyncio
nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, CallbackContext
import telegram.ext.filters as filters
import requests
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Scan QR Code", callback_data='scan')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Please choose:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'scan':
        await query.edit_message_text(text="Please send a photo of the QR code.")

async def scan_qr(update: Update, context: CallbackContext) -> None:
    photo = await update.message.photo[-1].get_file()
    await photo.download('qr_code.png')

    img = cv2.imread('qr_code.png')
    decoded_objects = decode(img)
    if decoded_objects:
        qr_data = decoded_objects[0].data.decode('utf-8')
        await update.message.reply_text(f'QR Code Data: {qr_data}')
        # Send data to backend
        requests.post('http://localhost:5000/scan', json={'data': qr_data})
    else:
        await update.message.reply_text('No QR code found.')

async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.PHOTO, scan_qr))

    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
