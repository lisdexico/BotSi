

from user import User
from consumption import Consumption

user1 = User('Le Tut')
user2 = User('Signe')

user1.add_consumption('Faraón', 0.25)
user1.add_consumption('Faraón', 0.25)
user1.remove_last_consumption()
user1.add_consumption('Faraón', 0.25)

user2.add_consumption('Q-dance', 0.5)
user2.add_consumption('Q-dance', 0.25)
user2.remove_last_consumption()
user2.remove_last_consumption()
user2.remove_last_consumption()
user2.remove_last_consumption()
user2.remove_last_consumption()
user2.remove_last_consumption()
user2.remove_last_consumption()
user2.add_consumption('Q-dance', 0.5)
user2.add_consumption('Q-dance', 0.25)
user2.remove_last_consumption()
user2.add_consumption('Q-dance', 0.5)
user2.add_consumption('Faraón', 0.25)

print()
print(user1)
print('hasn\'t consumed since' + str(user1.last_consumption_time))
user1.print_history()
user1.print_total()

print()

print(user2)
print('hasn\'t consumed since' + str(user2.last_consumption_time))
user2.print_history()
user2.print_total()

print()

user1.print_all()
user2.print_all()