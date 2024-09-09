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
    keyboard = [[InlineKeyboardButton("Scan QR Code", url='https://github.com/valenciavene/StoreSys/blob/master/templates/qr_scanner.html')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Please choose:', reply_markup=reply_markup)

async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
