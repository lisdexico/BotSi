
import fractions

class Consumption:

	def __init__(self, substance, quantity):
		self.substance = substance
		self.quantity = fractions.Fraction(quantity)

	def __str__(self):
		return str(self.quantity) + ' de ' + self.substance