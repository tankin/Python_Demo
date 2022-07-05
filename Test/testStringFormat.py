# -*- coding: utf-8 -*-

# example 1:
txt1 = "My name is {fname}, I'm {age}".format(fname = "John", age = 36)
print(txt1)

# example 2:
class T:
    def __init__(self):
        self.a = 1
        self.b = 2

t = T()
t.c = 3
print("{x.a}, {x.b}, {x.c}".format(x=t))
