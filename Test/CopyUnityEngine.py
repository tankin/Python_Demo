# -*- coding: utf-8 -*-

from Common import Util, SvnUtil
import traceback
import os


#################################################################################

def Main():
    argvs = Util.GetSysArg(1)
    unityVer = argvs[0]
    print(argvs)

    command = "net use \\\\192.168.40.10\\mlshare 123456 /user:share"
    Util.RunCmd(command)

    localPath = "C:\\Program Files"
    localUnityPath = os.path.join(localPath, unityVer)
    if os.path.isdir(localUnityPath):
        os.rename(localUnityPath, os.path.join(localPath, unityVer+"_bak"))

    remotePath = r"\\192.168.40.10\mlshare\工具\buildenv\DiskD\tools"
    Util.CopyDir(unityVer, remotePath, localPath)

   
#################################################################################

if __name__ == '__main__':
    try:
        before = Util.BeginTime_Sec("CopyUnityEngine")
        Main()
        Util.EndTime_Sec(before, "CopyUnityEngine")
    except Exception as e:
        print("!EXCEPTION!", e)
        traceback.print_exc()
    finally:
        print("-- CopyUnityEngine.py end --")