import random
from random import *
import datetime
import cmd
import json
from pprint import pprint

try:
    f = open('Data.json')
except FileNotFoundError:
    with open('Data.json', 'w') as w:
        json.dump({}, w)
    f = open('Data.json')
finally:
    with f:
        database = json.load(f)
        database.setdefault('users', [])
        data = database.setdefault('data', {})
        data.setdefault('command_list', [])
user = None


def find_user_name(database, name):
    for user in database['users']:
        if user['name'] == name:
            return user
    return None


class Main(cmd.Cmd):
    prompt = '>>> '

    @property
    def user(self):
        return user

    @property
    def database(self):
        return database

    def do_details(self, arg):
        print('Name:      ', self.user['name'])
        print('AccountID: ', self.user['id'])
        print('Nickname:  ', self.user['nickname'])

    def do_setpas(self, arg):
        self.user['password'] = input('Enter your new password: ')

    def do_userlist(self, arg):
        pprint([u['name'] for u in self.database['users']])

    def do_message(self, target_user):
        t_user = find_user_name(self.database, target_user)
        if t_user is None:
            return

        message = input('Message: ')
        t_user['messages'].append({
            'from': self.user['name'],
            'date': str(datetime.datetime.now()),
            'message': message
        })

    def do_mymessages(self, arg):
        pprint(self.user['messages'])

    def do_addcommand(self, arg):
        self.database['data']['command_list'].append(arg)

    def do_admin(self, arg):
        if not self.user['admin'] and arg == 'True':
            self.user['admin'] = True

    def do_delete(self, arg):
        if self.user['admin']:
            return

        delete = input('Are you sure you would like to delete your account: ')
        if delete != 'y':
            return

        i = self.database.index(self.user)
        self.database.pop(i)

        return True

    def do_signout(self, arg):
        return True


def signin():
    global user

    while True:
        existing_account = input('Do you have an existing account (y/n): ')
        if existing_account == 'y':
            username = input('Username: ')
            user = find_user_name(database, username)
            if user is None:
                print('Invalid username')
                continue

            password = input('Password: ')
            if password != user['password']:
                print('Invalid password')
                continue

            Main().cmdloop()
        else:
            username = str(input('Username: '))
            while not username:
                username = input("You haven't entered anything, try again.")

            user = find_user_name(database, username)
            if user is not None:
                print('That name already exists.')
                user = None
                continue

            password = input('Password: ')
            while len(password) < 4:
                print('Your password must be 5 characters long.')
                password = input('Password: ')

            nickname = input('Enter your nickname: ')
            id_ = random()
            while id_ in [u['id'] for u in database['users']]:
                id_ = random()

            user = {
                'name': username,
                'password': password,
                'nickname': nickname,
                'id': id_,
                'messages': [],
                'admin': False
            }
            database['users'].append(user)
            Main().cmdloop()


if __name__ == '__main__':
    try:
        signin()
    finally:
        with open('Data.json', 'w') as f:
            json.dump(database, f)
