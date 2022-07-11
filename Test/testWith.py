# -*- coding: UTF-8 -*-

import os
import shutil

with open("svnext.txt", 'w') as f:
    f.write("1111\n")
    f.write("2222\n")

path = "F:\\streees"
if os.path.isdir(path) :
    shutil.rmtree(path)

print("1111")