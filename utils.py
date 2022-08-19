from os import system
from sys import stdout, platform

class Utils:

    def clear():
        if platform == "linux" or platform == "linux2":
            system('clear')
        elif platform == "darwin":
            system('clear')
        elif platform == "win32":
            system('cls')

    def title():
        stdout.write("\x1b]2;Proxy Checker by Jag\x07")