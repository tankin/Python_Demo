# -*- coding: utf-8 -*-

import traceback
#import sth

if __name__ == '__main__':
    # get arguments
    x = 1
    try:
        # call functions
        print(x)        
    except Exception as e:
        exc_msg = traceback.format_exc() 
        print(exc_msg)
        exit(-1)