
import nest_asyncio
nest_asyncio.apply()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
import telegram.ext.filters as filters
import os
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the bot token from environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton("Scan QR Code", url='https://valenciavene.github.io/StoreSys/templates/qr_scanner.html')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Welcome! Please choose:', reply_markup=reply_markup)

async def handle_webapp_data(update: Update, context: CallbackContext) -> None:
    data = update.message.web_app_data.data
    await update.message.reply_text(f'QR Code Data: {data}')

async def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
