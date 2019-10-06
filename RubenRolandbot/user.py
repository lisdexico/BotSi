
import datetime
from consumption import Consumption

class User:

	def __init__(self, name):
		self.name = name
		self.history = dict()

	def __str__(self):
		return self.name

	def add_consumption(self, substance, quantity):
		consumption = Consumption(substance, quantity)
		self.history[datetime.datetime.now()] = consumption

	@property
	def last_consumption_time(self):
		return max(list(self.history.keys()))

	def delete_last_consumption(self):
		if self.history:
			del self.history[self.last_consumption_time]

	@property
	def totals(self):
		totals = dict()
		for consumption in list(self.history.values()):
			if consumption.substance in totals:
				totals[consumption.substance] += consumption.quantity
			else:
				totals[consumption.substance] = consumption.quantity
		return totals

	def history_to_str(self):
		string = 'Historial:\n\n'
		for key in self.history:
			string += '    - {0} a las {1}\n'.format(self.history[key], str(key.strftime('%H:%M')))
		return string

	def total_to_str(self):
		string = 'Total:\n'
		for key in self.totals:
			string += '    - {0}: {1}\n'.format(key, self.totals[key])
		return string

	def all_to_str(self):
		string = '\n' + '-----------------------------------\n'
		string += str(self) + '\n\n'
		string += '{0}\n{1}'.format(self.history_to_str(), self.total_to_str())
		return string
		


