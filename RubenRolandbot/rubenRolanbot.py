
import os
import suggestion_box
from controller import Controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler
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

# Stages of consversation
HISTORY, UNDO, DELETE_USER = range(3)

def user_selection_keyboard():
    keyboard = []
    for user in controller.users:
        keyboard.append([InlineKeyboardButton(user, callback_data=user)])
    return InlineKeyboardMarkup(keyboard)



################################################
# start
def start(update, context):
    update.message.reply_text(txt.start_text)


################################################
# help
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
# suggest
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
# add_user
def add_user(update, context):
    args = update.message.text.split()
    try:
        controller.add_user(args[1])
    except Exception: # If user couldn't be registered (e.g. not enough args)
        update.message.reply_text(txt.add_user_error)
    else:
        update.message.reply_text(txt.add_user_text)


################################################
# delete_user
def delete_user(update, context):
    reply_markup = user_selection_keyboard()
    update.message.reply_text('For which user?:', reply_markup=reply_markup)
    return DELETE_USER

def delete_user_callback(update, context):
    query = update.callback_query
    bot = context.bot
    controller.delete_user(query.data)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=txt.delete_user_text
    )
    return ConversationHandler.END


################################################
# users
def users(update, context):
    update.message.reply_text(controller.users_to_str())

################################################
# consume
def consume(update, context):
    args = update.message.text.split()
    try:
        controller.add_consumption(args[1], args[2], args[3])
    except Exception: # If consumption couldn't be registered (e.g. not enough args)
        update.message.reply_text(txt.consume_error)
    else:
        update.message.reply_text(txt.consume_text)


################################################
# history
def history(update, context):
    reply_markup = user_selection_keyboard()
    update.message.reply_text('For which user?:', reply_markup=reply_markup)
    return HISTORY

def history_callback(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=controller.history_to_str(query.data)
    )
    return ConversationHandler.END

################################################
# undo
def undo(update, context):
    reply_markup = user_selection_keyboard()
    update.message.reply_text('For which user?:', reply_markup=reply_markup)
    return UNDO

def undo_callback(update, context):
    query = update.callback_query
    bot = context.bot
    username = query.data
    controller.delete_last_consumption(username)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=txt.undo_text.format(username)
    )
    return ConversationHandler.END

################################################
# default
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
    dispatcher.add_handler(CommandHandler('add_user', add_user))
    dispatcher.add_handler(CommandHandler('users', users))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('history', history), CommandHandler('undo', undo), CommandHandler('delete_user', delete_user)],
        states={
            HISTORY: [CallbackQueryHandler(history_callback)],
            UNDO: [CallbackQueryHandler(undo_callback)],
            DELETE_USER: [CallbackQueryHandler(delete_user_callback)]
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dispatcher.add_handler(conv_handler)

    dispatcher.add_handler(MessageHandler(Filters.text, default))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()