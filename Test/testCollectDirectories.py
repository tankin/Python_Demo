# -*- coding: UTF-8 -*-

import os

p = "f:\\mlproj2017"
#for root, dirs, files in os.walk():
#    for d in dirs:
#        print(d)

#print(os.listdir(p))

#directories=[d for d in os.listdir(p) if os.path.isdir(d)]
#directories=[d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and d.find("lua") > 0]
#directories=[d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
#directories=[d for d in os.listdir(os.getcwd()) if os.path.isdir(d) and d.find("ml") >= 0]
#directories=[d for d in os.listdir("F:\\mlproj2017") if os.path.isdir(d) and d.find("ml") >= 0]
directories=[d for d in os.listdir(p) if os.path.isdir(os.path.join(p, d)) and d.find("Legends") >= 0]
print(directories)