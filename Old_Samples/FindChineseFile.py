#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# find the line of containing chinese in files
 
import re
import os

path = r"f:\mlproj2017\Assets"

'''
def start_find_chinese():
    find_count = 0
    with open('ko_untranslated.txt', 'wb') as outfile:
    with open('source_ko.txt', 'rb') as infile:
    while True:
    content = infile.readline()
    if re.match(r'(.*[\u4E00-\u9FA5]+)|([\u4E00-\u9FA5]+.*)', content.decode('utf-8')):
        outfile.write(content)
        find_count += 1;

    if not content:
        return find_count
''' 

def FindAllChineseFile(path):
    tagFiles = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if re.match(r'(.*[\u4E00-\u9FA5]+)|([\u4E00-\u9FA5]+.*)', f):
                tagFiles.append(root + "\\" +  f + '\n')
    return tagFiles


# start to find
if __name__ == '__main__':
    data = FindAllChineseFile(path)
    filePath = os.path.join(os.getcwd(),"trunk/AllChineseFiles.txt")
    print("path", filePath)
    with open(filePath, "w", encoding='UTF-8') as f:
        f.writelines(data)
    