# -*- coding: UTF-8 -*-

import os
import time

def RunCmd(cmd):
    print(cmd)
    code = os.system(cmd)
    return code
    
if __name__ == "__main__" :
    fromDir = "e:\\"
    toDir = "f:\\"
    fileName = "2021_Book_RayTracingGemsII.pdf"
    #robocopy .\ .\ProjectSettings Assembly-CSharp.csproj /mt

    oldFile = "%s\\%s" % (toDir, fileName)
    if os.path.isfile(oldFile) :
        os.remove(oldFile)

    t = time.time()

    #cmd = "robocopy %s %s %s" % (fromDir, toDir, fileName)
    cmd = "copy %s\\%s %s\\%s" % (fromDir, fileName, toDir, fileName)
    RunCmd(cmd)

    total = int(round((time.time()-t) * 1000))    
    print("time: %d" %(total))
