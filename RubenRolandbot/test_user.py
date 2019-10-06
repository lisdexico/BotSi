

from user import User
from consumption import Consumption

user1 = User('Le Tut')
user2 = User('Signe')

user1.add_consumption('Faraón', 0.25)
user1.add_consumption('Faraón', 0.25)
user1.delete_last_consumption()
user1.add_consumption('Faraón', 0.25)

user2.add_consumption('Q-dance', 0.5)
user2.add_consumption('Q-dance', 0.25)
user2.delete_last_consumption()
user2.delete_last_consumption()
user2.delete_last_consumption()
user2.delete_last_consumption()
user2.delete_last_consumption()
user2.delete_last_consumption()
user2.delete_last_consumption()
user2.add_consumption('Q-dance', 0.5)
user2.add_consumption('Q-dance', 0.25)
user2.delete_last_consumption()
user2.add_consumption('Q-dance', 0.5)
user2.add_consumption('Faraón', 0.25)

print()
print(user1)
print('hasn\'t consumed since' + str(user1.last_consumption_time))
print(user1.history_to_str())
print(user1.total_to_str())

print()

print(user2)
print('hasn\'t consumed since' + str(user2.last_consumption_time))
print(user2.history_to_str())
print(user2.total_to_str())

print()

print(user1.all_to_str())
print(user2.all_to_str())