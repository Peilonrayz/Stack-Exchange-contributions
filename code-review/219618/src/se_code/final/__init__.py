#!/usr/bin/python
"""
Program: Temperature Coversion (C to F, or F to C)
Date:    02 May 2019
Author:  Jason P. Karle
Remark:  This program was inspired by a Python exercise that
asks you to create a program that will convert one Celsius value to Fahrenheit;
so a program that can be executed with three lines of code.
However, I wanted to make something that would allow the user to
convert to and from either C of F, and do so multiple times, until the user
decides to end the program. This was also an exercise for me to
advance not only my code skills, but how I structure a program.
"""


def input_celsius(prompt):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print('That is not a number!')
        else:
            if value < -273.5 or value > 5.5**30:
                print('That is not a valid range.')
                continue
            return value


def c_to_f(value):
    return (value * (9 / 5)) + 32


def convert_c_to_f():
    print('\nThank you, please enter the')
    print('value you want to convert.')
    print('Enter a value between -273.5°C to')
    print('+5.5 dectillion °C')
    celsius = input_celsius(': ')
    fahrenheit = c_to_f(celsius)
    print(f'{celsius}°C equals: {fahrenheit}°F')


def input_fahrenheit(prompt):
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print('That is not a number!')
        else:
            if value < -459.5 or 42**30 < value:
                print('That is not a valid entry.')
                continue
            return value


def f_to_c(value):
    return (5 / 9) * (value - 32)


def convert_f_to_c():
    print('\nThank you, please enter the')
    print('value you want to convert.')
    print('Enter a value between -273.5°C to')
    print('+5.5 dectillion °C')
    fahrenheit = input_fahrenheit(': ')
    celsius = f_to_c(fahrenheit)
    print(f'{fahrenheit}°F equals: {celsius}°C')


def quit_continue():
    print('\nDo you want to:\n')
    print('     1. Make another conversion; or')
    print('     2. Exit the program?\n')
    answer = input('Make you selection: ')
    return answer == '1'


def main():
    while True:
        print('Please enter the number')
        print('corresponding to what you')
        print('want to convert:')
        print('     1. Celsius to Fahrenheit')
        print('     2. Fahrenheit to Celsius')
        print('     3. Exit\n')
        selection = input('Enter 1, 2 or 3: ')
        if selection == '1':
            convert_c_to_f()
        elif selection == '2':
            convert_f_to_c()
        else:
            return
        if not quit_continue():
            return


if __name__ == '__main__':
    print('Welcome to the temperature')
    print('conversion program!\n')
    main()
