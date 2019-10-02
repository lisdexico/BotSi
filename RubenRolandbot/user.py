
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

	def remove_last_consumption(self):
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

	def print_history(self):
		print('Historial:')
		for key in self.history:
			print('    - ' + str(self.history[key]) + ' a las ' + key.strftime('%H:%M') )

	def print_total(self):
		print('Totales:')
		for key in self.totals:
			print('    - ' + str(key) + ': ' + str(self.totals[key]) )

	def print_all(self):
		print('\n' + '-----------------------------------')
		print(str(self) + '\n')
		self.print_history()
		print()
		self.print_total()


