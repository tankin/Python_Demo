#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import shutil
import stat
import time


#argLength: how many args it should be, if less, it'll pump out error
def GetSysArg(argLength):
    if len(sys.argv) < argLength + 1:
        raise RuntimeError("Not enough system arguments! Current args length : %d" % (len(sys.argv) - 1))
    else:
        argvList = []
        ignoreFirst = True
        for i in sys.argv:
            if ignoreFirst :
                ignoreFirst = False
            else:
                argvList.append(i.strip())
        
        return argvList

# count by seconds, float number
def BeginTime_Sec(taskName):
    print(">> %s begin " % (taskName))
    return time.perf_counter()

def EndTime_Sec(beginTime, taskName):
    print("<< %s end " % (taskName))
    print("##### total time : %f #####" % (time.perf_counter() - beginTime))

################################################################################################

def RunCmd(cmd):
    print(cmd)
    code = os.system(cmd)
    if code == 1 :
        raise RuntimeError("Run Cmd Failed! [%s]" % (cmd))

def ErrorPrint(msg):
    print("[Error] : %s" % (msg))


################################################################################################

def CreateDir(dir):
    if not os.path.isdir(dir) :
        os.mkdir(dir)
        print("Create dir:" + dir)
            
    if os.path.isdir(dir):
        print(" -- Finish create Root Dir: %s -- " % (dir))
        return 0        
    else:
        print("[Error] : %s" % (dir))
        return 1


def on_rm_error( func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod( path, stat.S_IWRITE )
    os.unlink( path )

def RemoveDir(path):
    if os.path.isdir(path) :
        shutil.rmtree(path, onerror = on_rm_error)

def DelFile(path):
    if os.path.isfile(path) :
        os.remove(path)

def CopyDir(dirName, srcDir, destDir):
    fromPath = os.path.join(srcDir, dirName)
    toPath = os.path.join(destDir, dirName)
    print("From: " + fromPath)
    print("To: " + toPath)
    if os.path.isdir(toPath):
        print("> " + toPath + " already exists")
    else:
        shutil.copytree(fromPath, toPath)

def CopyFile(fileName, srcDir, destDir):
    fromPath = os.path.join(srcDir, fileName)
    toPath = os.path.join(destDir, fileName)
    print("From: " + fromPath)
    print("To: " + toPath)
    if os.path.isfile(toPath):
        print("> " + toPath + " already exists")
    else:
        if os.path.isfile(fromPath):
            shutil.copyfile(fromPath, toPath)

def CopyFileInSameDir(dir, srcFileName, destFileName):
    fromPath = os.path.join(dir, srcFileName)
    toPath = os.path.join(dir, destFileName)
    print("From: " + fromPath)
    print("To: " + toPath)
    if os.path.isfile(toPath):
        print("> " + toPath + " already exists")
    else:
        if os.path.isfile(fromPath):
            shutil.copyfile(fromPath, toPath)


def RenameFile(srcDir, srcFileName, destFileName):
    fromPath = os.path.join(srcDir, srcFileName)
    toPath = os.path.join(srcDir, destFileName)
    if os.path.isfile(toPath):
        print("> " + toPath + " already exists")
    else:
        if os.path.isfile(fromPath):
            os.rename(fromPath, toPath)
    


################################################################################################

def unzipFile(zipExe, fileName, fileDir, destDir):
    #baseName = os.path.splitext(fileName)[0]
    fromPath =  os.path.join(fileDir, fileName)
    if not os.path.isfile(fromPath):
        print("[Error]: " + fromPath + " doesn't exists, can't unzip")
    else:
        cmd = "%s x %s -o%s" % (zipExe, fromPath, destDir)
    return RunCmd(cmd)

def zipFile():
    pass
