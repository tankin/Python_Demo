# -*- coding: UTF-8 -*-

ver = "1.6.34_AI"
pos1 = ver.rfind('.')
pos2 = ver.find('_')
key = ver[pos1+1 : pos2]
print(key)