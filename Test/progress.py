# _*_ coding: utf-8 _*_

from time import sleep

def progress(percent = 0, width = 30):
    left = width * percent // 100
    right = width - left
    print('\r[', '#' * left, ' ' * right, ']', f'{percent: f}%', sep= '', end= '', flush = True)

for i in range(101):
    progress(i)
    sleep(0.1)