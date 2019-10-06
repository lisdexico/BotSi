
from consumption import Consumption
from user import User
from controller import Controller


ruben = Controller()

ruben.add_user('Le Tut')
ruben.add_user('Signe')
print(ruben.users_to_str())

ruben.add_user('Le Tut')
print(ruben.users_to_str())
ruben.delete_user('Le Tut')
print(ruben.users_to_str())
ruben.add_user('Le Tut')
print(ruben.users_to_str())

print()


ruben.add_consumption('Le Tut', 'Faraón', 0.25)
ruben.add_consumption('Le Tut', 'Faraón', 0.25)
ruben.add_consumption('Le Tut', 'Q-Dance', 0.25)
ruben.add_consumption('Le Tut', 'Faraón', 0.25)
ruben.add_consumption('Le Tut', 'Q-Dance', 0.25)
ruben.delete_last_consumption('Le Tut')
print(ruben.history_to_str('Le Tut'))

ruben.delete_last_consumption('Pepe')
ruben.delete_user('Pepe')
print(ruben.history_to_str('Pepe'))

ruben.add_consumption('Pepe', 'M', 1)
print(ruben.users_to_str())
print(ruben.history_to_str('Le Tut'))
print(ruben.history_to_str('Pepe'))