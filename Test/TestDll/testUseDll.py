# -*- coding: utf-8 -*-

from ctypes import*
import os


# load dynamic-link library
cwd = os.getcwd()
dllPath = os.path.join(cwd, "TestDll.dll")
print(dllPath)
mydll = cdll.LoadLibrary(dllPath)

# use the function in dll
if mydll is not None:
    result1= mydll.add(10,1)
    result2= mydll.subtract(10,1)
    print("Addition value:" + str(result1))
    print("Substraction:" + str(result2))