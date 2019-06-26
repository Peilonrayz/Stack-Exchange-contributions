import random
from random import *
import datetime
import string
import os
import getpass
global usernames
global passwords
global jointPassList
usernames = [line.strip()for line in open('Data/names.txt', 'r')]
passwords = [line.strip()for line in open('Data/passwords.txt', 'r')]
isAdmin = [line.strip()for line in open('Data/isAdmin.txt', 'r')]
accountIDs = [line.strip()for line in open('Data/accountIDs.txt', 'r')]
nicknames = [line.strip()for line in open('Data/nicknames.txt', 'r')]
jointPassList ='\n'.join(map(str, passwords))

def main():
                print('\n')
                print('\n')
                print('/help (1/2) for help')
                currentUserIndex = usernames.index(ascname)
                command =input('>>>')
                if command =='/help':

                                print('/signout       | sign out\n/details        | account details\n/setpas        | set password\n/userlist     | all users\n/mymessages | your messages\n/message | message\n/addcommand | add command')
                                input()
                                main()
                if command =='/details':

                                print('Name:      ', ascname)
                                print('AccountID: ', accountIDs[currentUserIndex])
                                print('Nickname:  ', nicknames[currentUserIndex])
                                input()
                                main()
                if command =='/setpas':

                                newpas =input('Enter your new password: ')
                                passwords[currentUserIndex] = newpas
                                jointPassList ='\n'.join(map(str, passwords))
                                openfile =open('Data/passwords.txt', 'w')
                                openfile.write(jointPassList)
                                openfile.close()
                                input()
                                main()
                if command =='/userlist':
                                userlist =open('Data/names.txt').read()
                                print(userlist)
                                input()
                                main()
                if command =='/message':
                                whatuser =input('What user: ')
                                if whatuser in usernames:
                                    message =input('What message would you like to send: ')
                                    openfile =open('Data/messages/recieved/'+whatuser+'.txt', 'a')
                                    date = str(datetime.datetime.now())
                                    openfile.write(date + ' : ')
                                    openfile.write(message+'\n')
                                    openfile.close()
                                    input()
                                    main()

                                elif whatuser not in usernames:
                                                print('Nobody was found.')
                                                input()
                                                main()

                if command =='/mymessages':
                                messagesList = [line.strip()for line in open('Data/messages/recieved/'+ascname+'.txt', 'r')]
                                messages = '\n'.join(messagesList)
                                print(messages)
                                input()
                                main()

                if command =='/addcommand':
                                openfile =open('Data/addCommandList.txt', 'a')
                                addcommand =input('What would you like see added to this database: ')
                                openfile.write(addcommand+'\n')
                                openfile.close()
                                input()
                                main()

                if command =='/admin':
                                print(isAdmin[currentUserIndex])
                                if isAdmin[currentUserIndex] =='True':
                                                print('Nice :)')
                                                input()
                                                main()

                                elif isAdmin[currentUserIndex] =='False':
                                                print('You are not an Admin')
                                                change =input()
                                                if change =='False':
                                                                isAdmin[currentUserIndex] = True
                                                                main()
                                                else:
                                                                main()

                                if isAdmin[currentUserIndex] =='False':
                                                delete =input('Are you sure you would like to delete your account: ')
                                                if delete =='y':
                                                                accountIDs.remove(accountIDs[currentUserIndex])
                                                                isAdmin.remove(isAdmin[currentUserIndex])
                                                                usernames.remove(usernames[currentUserIndex])
                                                                passwords.remove(passwords[currentUserIndex])
                                                                nicknames.remove(nicknames[currentUserIndex])
                                                                os.remove('Data/messages/recieved/'+ascname+'.txt')
                                                                openfile = open('Data/names.txt', 'w')
                                                                openfile.write(name + '\n')
                                                                openfile.close()

                                                                openfile = open('Data/accountIDs.txt', 'w')
                                                                openfile.write(str(accountID) + '\n')
                                                                openfile.close()

                                                                openfile = open('Data/nicknames.txt', 'w')
                                                                openfile.write(nickname + '\n')
                                                                openfile.close()

                                                                openfile = open('Data/passwords.txt', 'w')
                                                                openfile.write(password + '\n')
                                                                openfile.close()

                                                                openfile = open('Data/isAdmin.txt', 'w')
                                                                openfile.write(adminFalse + '\n')
                                                                openfile.close()
                                                                print('Complete...')
                                                                signin()


                if command =='/signout':

                                areYouSure =input('Are you sure you would like to sign out(y/n): ')
                                if areYouSure =='y':
                                                print('Signing out\n.\n.\n.')
                                                signin()
                                elif areYouSure =='n':
                                                main()
                                else:
                                                main()


                else:
                                print(command, 'is not a command in our library, type /addcommand to request new command.')
                                input()
                                main()

def signin():
                existingAccount =input('Do you have an existing account (y/n): ')
                if existingAccount =='y':
                                global ascname
                                global ascpass
                                ascname =input('Enter your username: ')
                                currentUsername = ascname
                                if ascname in usernames:
                                                userIndex = usernames.index(ascname)
                                                print('Correct username.')
                                                ascpass =input('Enter your password: ')
                                                while ascpass in passwords:
                                                                passcheck = passwords.index(ascpass)
                                                                if userIndex == passcheck:
                                                                                print('welcome back', ascname + '.')
                                                                                main()

                                                                else:
                                                                                wrongPass =input('Incorrect password.')
                                                                                input()
                                                                                signin()
                                                print('Yes')
                                                wrongPass =input('Incorrect password.')
                                                input()
                                                signin()
                                elif ascname not in usernames:
                                                wrongName =input('Incorrect username.')
                                                input()
                                                signin()
                                else:
                                                #debuging
                                                print('Error')
                                                singin()

                elif existingAccount =='n':
                                name =str(input('Enter your name: '))
                                while len(name) == 0:
                                                name =input("You haven't entered anything, try again.")
                                                input()
                                                signin()
                                if name in open('Data/names.txt').read():
                                                name =input('That name already exists.')
                                                input()
                                                signin()
                                usernames.append(name)
                                password =input('Enter your new password: ')
                                while len(password) < 4:
                                                password =input('Your password must be 5 characters long.')
                                                input()
                                                signin()
                                passwords.append(password)

                                nickname =input('Enter your nickname: ')
                                accountID =random()
                                while accountID in accountIDs:
                                                accountID =random()

                                adminFalse = str(False)
                                isAdmin.append(adminFalse)

                                openfile = open('Data/messages/recieved/' +name+ '.txt',  'w+')
                                openfile.write('\n')
                                openfile.close()

                                openfile = open('Data/names.txt', 'a')
                                openfile.write(name + '\n')
                                openfile.close()

                                openfile = open('Data/accountIDs.txt', 'a')
                                openfile.write(str(accountID) + '\n')
                                openfile.close()

                                openfile = open('Data/nicknames.txt', 'a')
                                openfile.write(nickname + '\n')
                                openfile.close()

                                openfile = open('Data/passwords.txt', 'a')
                                openfile.write(password + '\n')
                                openfile.close()

                                openfile = open('Data/isAdmin.txt', 'a')
                                openfile.write(adminFalse + '\n')
                                openfile.close()



                                signin()

                else:
                                signin()

signin()