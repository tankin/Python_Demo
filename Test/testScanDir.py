# -*- coding: utf-8 -*-

from datetime import datetime
from os import scandir

def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime("%d %b %Y")
    return formated_date

dir_entries = scandir(r"f:\XLua\build64")
for entry in dir_entries:
    if entry.is_file():
        info = entry.stat()
        print(f"{entry.name}\t [File] \tLast Modified: {convert_date(info.st_mtime)}")

    if entry.is_dir():
        info = entry.stat()
        print(f"{entry.name}\t [Dir] \tLast Modified: {convert_date(info.st_mtime)}")