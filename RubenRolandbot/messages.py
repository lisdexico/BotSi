

start_text = '''\
Hi there, I am Ruben Rolanbot.

I don't like my name so feel free to suggest a new one.

My purspouse is to help you keep track of how much you consume, so you don't overdo yourself.

To see available commands, use /help.

If you find any bugs or have any ideas as to how I could provide a better experience, plese let me know using the command /suggest \
'''

start_description = 'Displays welcome message.'

help_description = 'Displays this (duh).'

help_text = 'These are the available commands:'

suggest_description = 'Takes a suggestion on how to improve this bot.'

suggestion_box_full = 'Oops, looks like our suggestions box is full!\n Feel free to contact the administrator and tell him to get off his ass.'

suggestion_recieved = 'Thank you so much for your suggestion, we\'ll take a look at it as soon as possible'

add_user_error = 'Sorry, an error occurred, we could not register the user.'

add_user_text = 'User registered.'

delete_user_error = 'Sorry, an error occurred, we could not delete the user.'

delete_user_text = 'User deleted.'

consume_description = '''Registers a consumption. Takes user, substance and quantity as arguments, separated only by space.
 For example, '/consume Signe pasta 0.5' would register that Signe consumed half a plate of pasta.
 This command must not be used in the house of Mr. Parra'''

consume_text = 'Consumption registered.'

consume_error = 'Sorry, an error occurred, we could not register the consumption.'

history_description = '''Displays the consumptions taken by a user (whose name must be provided as an argument).
 For example, '/history Signe' would tell us that he just had some pasta (see /consume). '''

history_error = 'Sorry, we could not retrieve history for that user, please try again later.'

undo_description = 'Deletes the last consumption for the specified user.'

undo_error = 'Sorry, we could not delete the last entry for the specified user, please try again later.'

undo_text = 'Last consumption for {} has been deleted.'

unknown_command = '''Sorry, I don't know that command. To see which ones are available use /help'''
