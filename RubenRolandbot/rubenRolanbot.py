
import os
import suggestion_box
from controller import Controller
from telegram import InlineKeyboardButton, InlineKeyboardMarkup,  KeyboardButton, ReplyKeyboardMarkup, ForceReply
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
MAIN_MENU, HISTORY, UNDO, ADD_USER, DELETE_USER, SUGGEST, CONSUME, ABOUT, HELP, START_OVER, SUBSTANCE, QUANTITY = range(12)

# Commands available
commands = ['start', 'help', 'add_user', 'delete_user', 'users', 'consume', 'history', 'undo', 'suggest', 'about']

################################################
# Keyboards
def user_selection_keyboard():
    keyboard = []
    for user in controller.users:
        keyboard.append([InlineKeyboardButton(user, callback_data=user)])
    return InlineKeyboardMarkup(keyboard)

def main_menu_keyboard():
    keyboard = []
    for command in commands:
        if command != 'start':
            keyboard.append([InlineKeyboardButton(command, callback_data=command)])
    return InlineKeyboardMarkup(keyboard)

def start_over_keyboard():
    keyboard = [[InlineKeyboardButton('Start over', callback_data='start_over')]]
    return InlineKeyboardMarkup(keyboard)

################################################
# Texts

def help_text():
    string = txt.help_text
    for key in txt.command_descriptions:
        string += '\n\n - {0}: {1}'.format(key, txt.command_descriptions[key])
    return string

def static_text(command):
    def neat_trick():
        return txt.texts[command]
    return neat_trick

def users_text():
    return controller.users_to_str()

texts = {
    'start': static_text('start'),
    'help': help_text,
    'add_user': static_text('add_user'),
    'delete_user': static_text('delete_user'),
    'users': users_text,
    'suggest': static_text('suggest'), 
    'consume': static_text('consume'),
    'history': static_text('history'),
    'undo': static_text('undo'),
    'about': static_text('about'),
}

keyboards = {
    'start': main_menu_keyboard,
    'help': start_over_keyboard,
    'add_user': ForceReply,
    'delete_user': user_selection_keyboard,
    'users': start_over_keyboard,
    'suggest': ForceReply, 
    'consume': user_selection_keyboard,
    'history': user_selection_keyboard,
    'undo': user_selection_keyboard,
    'about': start_over_keyboard,
}

next_state = {
    'start': MAIN_MENU,
    'help': START_OVER,
    'add_user': ADD_USER,
    'delete_user': DELETE_USER,
    'users': START_OVER,
    'suggest': SUGGEST, 
    'consume': CONSUME,
    'history': HISTORY,
    'undo': UNDO,
    'about': START_OVER,
}

################################################
# start
def start(update, context):
    update.message.reply_text(texts['start'](), reply_markup=main_menu_keyboard())
    return MAIN_MENU

def start_callback(update, context):
    query = update.callback_query
    bot = context.bot
    option = query.data
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=texts[option](),
        reply_markup=keyboards[option]()
    )
    return next_state[option]

def start_over_callback(update, context):
    query = update.callback_query
    bot = context.bot
    option = 'start'
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=texts[option](),
        reply_markup=keyboards[option]()
    )
    return MAIN_MENU

################################################
# suggest
suggestions = suggestion_box.SuggestionBox()

def suggest(update, context):
    try:
        suggestions.write_suggestion(update.message.from_user.username, update.message.text)
    except suggestion_box.SuggestionBoxFull:
        update.message.reply_text(txt.suggestion_box_full, reply_markup=start_over_keyboard())
    else:
        update.message.reply_text(txt.suggestion_recieved, reply_markup=start_over_keyboard())
    finally:
        return START_OVER


################################################
def add_user(update, context):
    try:
        controller.add_user(update.message.text)
    except Exception: # If user couldn't be registered (e.g. not enough args)
        update.message.reply_text(text=txt.add_user_error, reply_markup=start_over_keyboard())
    else:
        update.message.reply_text(text=txt.user_added_text, reply_markup=start_over_keyboard())
    finally:
        return START_OVER

################################################
def delete_user_callback(update, context):
    query = update.callback_query
    bot = context.bot
    controller.delete_user(query.data)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=txt.user_deleted_text,
        reply_markup=start_over_keyboard()
    )
    return START_OVER

################################################
# consume

consumption = ['name_placeholder', 'substance_placeholder', 'quantity_placeholder']

def consume_callback(update, context):
    query = update.callback_query
    bot = context.bot
    consumption[0] = query.data
    bot.send_message(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text='Type in the substance (can use pseudonym)',
        reply_markup=ForceReply()
    )
    return SUBSTANCE

def substance(update, context):
    consumption[1] = update.message.text
    bot = context.bot
    bot.send_message(
        chat_id=update.message.chat_id,
        message_id=update.message.message_id,
        text='Type in the quantity (number)',
        reply_markup=ForceReply()
    )
    return QUANTITY

def quantity(update, context):
    consumption[2] = update.message.text
    controller.add_consumption(consumption[0], consumption[1], consumption[2])
    bot = context.bot
    bot.send_message(
        chat_id=update.message.chat_id,
        message_id=update.message.message_id,
        text='Consumption added',
        reply_markup=start_over_keyboard()
    )
    return START_OVER

# def consume(update, context):
#     args = update.message.text.split()
#     try:
#         controller.add_consumption(args[1], args[2], args[3])
#     except Exception: # If consumption couldn't be registered (e.g. not enough args)
#         update.message.reply_text(txt.consume_error)
#     else:
#         update.message.reply_text(txt.consume_text)


################################################
# history
def history_callback(update, context):
    query = update.callback_query
    bot = context.bot
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=controller.history_to_str(query.data),
        reply_markup=start_over_keyboard()
    )
    return START_OVER

################################################
# undo
def undo_callback(update, context):
    query = update.callback_query
    bot = context.bot
    username = query.data
    controller.delete_last_consumption(username)
    bot.edit_message_text(
        chat_id=query.message.chat_id,
        message_id=query.message.message_id,
        text=txt.undo_text.format(username),
        reply_markup=keyboards['undo']
    )
    return START_OVER

################################################
# default
def default(update, context):
    update.message.reply_text(txt.unknown_command)


def main():
    # Create bot
    API_TOKEN = os.environ.get('RUBEN_TOKEN')
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MAIN_MENU: [CallbackQueryHandler(start_callback)],
            START_OVER: [CallbackQueryHandler(start_over_callback)],
            HISTORY: [CallbackQueryHandler(history_callback)],
            UNDO: [CallbackQueryHandler(undo_callback)],
            DELETE_USER: [CallbackQueryHandler(delete_user_callback)],
            ADD_USER: [MessageHandler(Filters.text, add_user)],
            SUGGEST: [MessageHandler(Filters.text, suggest)],
            CONSUME: [CallbackQueryHandler(consume_callback)],
            SUBSTANCE: [MessageHandler(Filters.text, substance)],
            QUANTITY: [MessageHandler(Filters.text, quantity)],
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