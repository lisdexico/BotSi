
###############################################################
###############################################################
###############################################################
#

import os
from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

API_TOKEN = os.environ.get('HELLO_WORLD_TOKEN')
updater = Updater(token=API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
	context.bot.send_message(chat_id=update.message.chat_id,
		text="Hello world.\nHumans made me.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


