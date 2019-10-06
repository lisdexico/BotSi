

from consumption import Consumption
from user import User

class Controller:

	def __init__(self):
		self.users =  dict()

	def has(self, name):
		return name in self.users

	def add_user(self, name):
		if name not in self.users:
			self.users[name] = User(name)

	def delete_user(self, name):
		if name in self.users:
			del self.users[name]

	def add_consumption(self, name, substance, quantity):
		if name not in self.users:
			self.add_user(name)
		self.users[name].add_consumption(substance, quantity)

	def delete_last_consumption(self, name):
		if name in self.users:
			self.users[name].delete_last_consumption()

	def users_to_str(self):
		string = 'Users:\n'
		for user in self.users:
			string += '    - {}\n'.format(user)
		return string

	def history_to_str(self, name):
		if name in self.users:
			return self.users[name].all_to_str()
		else:
			return 'User not found'

