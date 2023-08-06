"""
Colorr Module for Python
~~~~~~~~~~~~~~~~~~~

A module that 
Can pick a color from a choice of 5;
Can save them to a list of colors used;
Can retreive the list of colors used;
Its pretty good.

(c) 2019 ItzAfroBoy.
MIT License
"""

__title__ = 'colorr'
__author__ = 'ItzAfroBoy'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2019 ItzAfroBoy'
__version__ = '1.0.2'

import random
import time


class Setup:
    def __init__(self, color_1, color_2, color_3, color_4, color_5):
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.color_4 = color_4
        self.color_5 = color_5
        self.colors = []

        self.add()

    def add(self):
        self.colors.append('#' + self.color_1)
        self.colors.append('#' + self.color_2)
        self.colors.append('#' + self.color_3)
        self.colors.append('#' + self.color_4)
        self.colors.append('#' + self.color_5)

    def choose(self):
        time.sleep(2)
        print(random.choice(self.colors))

    def check(self, i):
        file = open("colors.txt", 'r')
        p = i + '\n'
        if p in file.readlines():
            return True
        else:
            return False

    def save(self):
        file = open("colors.txt", 'a')
        for i in self.colors:
            if self.check(i) == True:
                return 
            else:
                file.write(i + '\n')
        file.close()

    def show(self):
        file = open("colors.txt", 'r')
        for i in file.readlines():
            print(i[:-1])
        file.close()

flomp = Setup("3C1518", "69140E", "A44200", "D58936", "FFF94F")