# -*- coding: utf-8 -*-

l = ["1", "2", "3"]
with open("t.txt", 'w') as f:
    f.writelines(l)
