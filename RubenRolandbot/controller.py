

from consumption import Consumption
from user import User

class Controller:

	def __init__(self):
		self.users =  dict()

	def add_user(self, name):
		if name not in self.users:
			self.users[name] = User(name)

	def remove_user(self, name):
		if name in self.users:
			del self.users[name]

	def add_consumption(self, name, substance, quantity):
		if name not in self.users:
			self.add_user(name)
		self.users[name].add_consumption(substance, quantity)

	def remove_last_consumption(self, name):
		if name in self.users:
			self.users[name].remove_last_consumption()

	def print_users(self):
		print('Users:')
		for user in self.users:
			print('    - ' + str(user))

	def print_history(self, name):
		if name in self.users:
			self.users[name].print_all()

