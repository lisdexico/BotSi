
import os
import telebot

class SuggestionBoxFull(Exception):
		pass

class SuggestionBox:

	def __init__(self, path='suggestions.txt', max_size=10000):
		self.path = path
		self.max_size = max_size

	def is_full(self):
		if os.path.isfile(self.path):
			if os.stat(self.path).st_size > self.max_size:
				return True
		return False

	@staticmethod
	def format_suggestion(user, suggestion):
		line = '---------------------------------------------------------------\n'
		return line + 'User: {}\n'.format(user) + suggestion + '\n\n\n'

	def write_suggestion(self, user, message):
		if self.is_full():
			raise SuggestionBoxFull('Error while trying to write suggestion box at ' + str(self.path) + ': max size of file exceeded.')
		with open(self.path, 'a') as f:
			f.write(SuggestionBox.format_suggestion(user, message))