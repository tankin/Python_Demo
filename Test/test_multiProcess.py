# -*- coding: utf-8 -*-

import os
import time
from multiprocessing import Pool

#print(os.cpu_count())

def test(p):
    print(p)    
    time.sleep(3)
    return p*2

def run():
    pool = Pool(10)
    for i in range(500):
        pool.apply(test, args=(i,))
        #pool.apply_async(test, args=(i,))
    print('test')
    pool.close()
    pool.join()

def runMap():
    pool = Pool(10)
    lists= [1, 2, 3]
    out = []
    out = pool.map(test, lists)
    print('begin')
    print(out)
    print('end')
    pool.close()
    pool.join()

if __name__ == "__main__":
    runMap()
