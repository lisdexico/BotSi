
from consumption import Consumption
from user import User
from controller import Controller


ruben = Controller()

ruben.add_user('Le Tut')
ruben.add_user('Signe')
ruben.print_users()

ruben.add_user('Le Tut')
ruben.print_users()
ruben.remove_user('Le Tut')
ruben.print_users()
ruben.add_user('Le Tut')
ruben.print_users()

print()


ruben.add_consumption('Le Tut', 'Faraón', 0.25)
ruben.add_consumption('Le Tut', 'Faraón', 0.25)
ruben.add_consumption('Le Tut', 'Q-Dance', 0.25)
ruben.add_consumption('Le Tut', 'Faraón', 0.25)
ruben.add_consumption('Le Tut', 'Q-Dance', 0.25)
ruben.remove_last_consumption('Le Tut')
ruben.print_history('Le Tut')

ruben.remove_last_consumption('Pepe')
ruben.remove_user('Pepe')
ruben.print_history('Pepe')

ruben.add_consumption('Pepe', 'M', 1)
ruben.print_users
ruben.print_history('Le Tut')
ruben.print_history('Pepe')