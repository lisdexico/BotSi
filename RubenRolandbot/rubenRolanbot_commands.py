
import os
import suggestion_box
from controller import Controller
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import messages as txt
import logging


################################################
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


################################################
# Backend inizialization 
controller = Controller()


################################################
# Start
def start(update, context):
    update.message.reply_text(txt.start_text)


################################################
# Help
commands = {'start': txt.start_description,
             'help': txt.help_description,
             'suggest': txt.suggest_description, 
             'consume': txt.consume_description,
             'history': txt.history_description,
             'undo': txt.undo_description}

def help(update, context):
    string = txt.help_text
    for key in commands:
        string += '\n\n - /{0}: {1}'.format(key, commands[key])
    update.message.reply_text(string)


################################################
# Suggest
suggestions = suggestion_box.SuggestionBox()

def suggest(update, context):
    try:
        suggestion = update.message.text.split(' ', 1)[1] # Don't want to save the command
    except Exception: # If suggestion couldn't be parsed (e.g. no suggestion)
        suggestion = '-'
    try:
        suggestions.write_suggestion(update.message.from_user.username, suggestion)
    except suggestion_box.SuggestionBoxFull:
        update.message.reply_text(txt.suggestion_box_full)
    else:
        update.message.reply_text(txt.suggestion_recieved)


################################################
# Consume
def consume(update, context):
    args = update.message.text.split()
    try:
        controller.add_consumption(args[1], args[2], args[3])
    except Exception: # If consumption couldn't be registered (e.g. not enough args)
        update.message.reply_text(txt.consume_error)
    else:
        update.message.reply_text(txt.consume_text)


################################################
# History
def history(update, context):
    args = update.message.text.split()
    try:
        update.message.reply_text(controller.history_to_str(args[1]))
    except Exception: # If history couldn't be retrieved (e.g. no username)
        update.message.reply_text(txt.history_error)

################################################
# Undo
def undo(update, context):
    args = update.message.text.split()
    try:
        controller.delete_last_consumption(args[1])
    except Exception: # If last entry couldn't be deleted (e.g. no username)
        update.message.reply_text(txt.undo_error)
    else:
        update.message.reply_text(txt.undo_text.format(args[1]))


################################################
# Default
def default(update, context):
    update.message.reply_text(txt.unknown_command)


def main():
    # Create bot
    API_TOKEN = os.environ.get('RUBEN_TOKEN')
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(CommandHandler('suggest', suggest))
    dispatcher.add_handler(CommandHandler('consume', consume))
    dispatcher.add_handler(CommandHandler('history', history))
    dispatcher.add_handler(CommandHandler('undo', undo))
    dispatcher.add_handler(MessageHandler(Filters.text, default))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()