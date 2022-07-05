# -*- coding: utf-8 -*-
import os
from xml.etree.ElementInclude import include

def SearchAllFiles(dirPath, csList):
    includeFile = ["ScreenWrap", "MaterialWrap", "ShaderWrap"]
    for root,dirs,files in os.walk(dirPath):
        for f in files:
            isInclude = False
            for one in includeFile :                
                if f.find(one) > -1 :
                    isInclude = True

            if f.startswith("UnityEngine") and f.endswith("Wrap.cs") and isInclude:
                csList.append(root+"\\"+f)


dirPath = r"F:\mygame_1.0.0.0.1\Assets\Scripts\CSharp\Game\XLua\Gen"
allFiles = []
SearchAllFiles(dirPath, allFiles)

for f in allFiles:
    print(f)
    cmd = "svn revert " + f
    os.system(cmd)