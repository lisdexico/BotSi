
###############################################################
###############################################################
###############################################################
#


from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token='720628059:AAFGhR0c63xW2DbneoZAVPj2O4lFNDddjRc', use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
	context.bot.send_message(chat_id=update.message.chat_id,
		text="Hello world.\nHumans made me.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()


