# -*- coding: utf-8 -*-


from ntpath import realpath
import os

with open("uselessArtFiles.txt", "r", encoding='UTF-8') as f:
    size = 0
    while True:
        relPath = f.readline()
        if not relPath:
            break

        realPath = "f:\\mlproj2017\\" + relPath
        realPath = realPath.replace('\n', '')
        if os.path.isfile(realPath):
            fsize = os.path.getsize(realPath)
            size += fsize
            print(fsize, size)

print("final : ", size)
print("-- %f MB -- " % (size / 1024 /1024))
print("-- %f GB -- " % (size / 1024 /1024 / 1024))