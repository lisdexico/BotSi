
import os
import telebot
import suggestion_box

API_TOKEN = os.environ.get('RUBEN_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


###########################################################
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am Ruben Rolanbot.
I don't like my name so feel free to suggest a new one.
My purspouse is to help you keep track of how much you consume, so you don't overdo yourself.
If you find any bugs or have any ideas as to how I could provide a better experience, plese let me know using the command /suggest \
""")


###########################################################
# Handle '/suggest'
suggestions = suggestion_box.SuggestionBox()

@bot.message_handler(commands=['suggest'])
def recieve_suggestion(message):
	user = message.from_user.username
	suggestion = message.text.split(' ', 1)[1]
	try:
		suggestions.write_suggestion(user, suggestion)
	except suggestion_box.SuggestionBoxFull:
		bot.reply_to(message, 'Oops, looks like our suggestions box is full!\n Feel free to contact the administrator and tell him to get off his ass.')
	except Exception:
		bot.reply_to(message, 'Sorry! An error ocurred and we could not take note of your suggestion, please try again later')
	else:
		bot.reply_to(message, 'Thank you so much for your suggestion, we\'ll take a look at it as soon as possible')

###########################################################


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.polling()