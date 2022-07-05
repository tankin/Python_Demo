# -*- coding: utf-8 -*-

from datetime import datetime

t0 = datetime.now()
print()
t1 = datetime.fromisoformat("2022-01-28 00:05:23")
print((t0-t1).total_seconds())
#print("1")
#assert 1 != 1, "not right"
#print("2")

def greet(*names):
    for n in names:
        print(n)

#greet("t1", "t2", "t3", "t4")
#greet(["t1", "t2", "t3", "t4"])


class Person:
    name = "John"

    def setAge(self):
        setattr(self, "age", 40)

p = Person()
p.setAge()
print(p.age)




