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


def quitContinue():
    print("\nDo you want to:\n")
    print("     1. Make another conversion; or")
    print("     2. Exit the program?\n")
    answer = input("Make you selection: ")
    try:
        if answer == "1":
            mainProg()
        else:
            return
    except:
        print("That is not a valid choice.")
        quitContinue()


def CtoF_Calc():
    print("\nThank you, please enter the")
    print("value you want to convert.")
    print("Enter a value between -273.5°C to")
    print("+5.5 dectillion °C")
    value = float(input(": "))
    try:
        if value < -273.5 or value > 5.5**30:
            print("That is not a valid range.")
            celciusCalc()
        else:
            answer = (value*(9/5))+32
            print(f"{value}°C equals: {answer}°F")
            quitContinue()
    except:
        print("Please entet a number!")
        CtoF_Calc()


def FtoC_Calc():
    print("\nThank you, please enter the")
    print("value you want to convert.")
    print("Enter a value between -273.5°C to")
    print("+5.5 dectillion °C")
    value = float(input(": "))
    try:
        if value < -459.5 or value > 42**30:
            print("That is not a valid entry.")
            celciusCalc()
        else:
            answer = (5/9)*(value-32)
            print(f"{value}°F equals: {answer}°C")
            quitContinue()
    except:
        print("That is not a number!\n")
        FtoC_Calc


def makeSelection(selection):
    try:
        if selection == "1":
            CtoF_Calc()
        elif selection == "2":
            FtoC_Calc()
        else:
            return
    except:
        print("That is not a valid selection")
        makeSelection(selection)


def mainProg():
    print("Please enter the number")
    print("corresponding to what you")
    print("want to convert:")
    print("     1. Celcius to Farenheit")
    print("     2. Farenheit to Celcius")
    print("     3. Exit\n")
    selection = input("Enter 1, 2 or 3: ")
    makeSelection(selection)


if __name__ == "__main__":
    print("Welcome to the temperature")
    print("conversion program!\n")
    mainProg()