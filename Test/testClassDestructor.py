# -*- coding: utf-8 -*-

class Emp:
    def __init__(self):
        print("create Emp")

    def __del__(self):
        print("destroy Emp")

e = Emp()