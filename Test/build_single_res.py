# -*- coding: utf-8 -*-

from Common import Util, SvnUtil
import os
import sys
import traceback


UnityPath = "\"C:\\Program Files\\Unity20170421\\Editor\\Unity.exe\""     # 237
#UnityPath = "C:\\Unity\\Editor\\Unity.exe"        # local
BuildLogFile = "D:\\res_single.log"

#################################################################################

def ReadLastSvnCollectVersion(projectPath, platform):
    svn_ver_path = os.path.join(projectPath, "res_single/%s/svn_ver_collect.txt" % (platform))
    with open(svn_ver_path, "r", encoding="UTF-8") as f:
        last = f.readline()
        last = last.replace("\r\n", "")
        return last

def WriteLastSvnVersion(projectPath, verNum, platform):
    svn_ver_path = os.path.join(projectPath, "res_single/%s/svn_ver.txt" % (platform))
    with open(svn_ver_path, "w", encoding="UTF-8") as f:
        f.write(verNum)

def SvnDelAllFiles(projectPath, platform):
    del_path = os.path.join(projectPath, "res_single_del.txt")
    with open(del_path, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\\", "/")
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            pos = line.rfind("/")
            fileName = line[pos + 1:]
            fileName = fileName.replace(".prefab", ".unity3d")
            
            dir = ""
            if line.find("Assets/Art/") > -1:
                dir = "art/"
            if line.find("Assets/UI/") > -1:
                dir = "ui/"

            filePath = os.path.join(projectPath, "res_single/%s/" % (platform) + dir + fileName)
            filePath = filePath.replace("\\", "/")
            if os.path.isfile(filePath):
                SvnUtil.Svn_Del(filePath)
            else:
                print("Warning: SvnDelAllFiles, file not exist, %s" % (filePath))
            
            filePath = filePath + ".manifest"
            if os.path.isfile(filePath):
                SvnUtil.Svn_Del(filePath)
            else:
                print("Warning: SvnDelAllFiles, file not exist, %s" % (filePath))

def Main():
    argvs = Util.GetSysArg(3)
    ver = argvs[0]
    svnComment = argvs[1]
    platform = argvs[2]
    print(argvs)

    ProjectPath = "G:/autobuild/Android-%s/mobaclient-%s_singleRes_%s" % (ver,ver,platform)
    usingFunc = "BuildAssetsByFile"
    rawFile = "res_single_raw.txt"
    target = "Android"
    if platform == "windows":
        target = "Win64"

    if not os.path.isdir(ProjectPath):
        print("[Error], dir not exist : %s" % (ProjectPath))
        return

    resSinglePath = os.path.join(ProjectPath, "res_single")
    if not os.path.isdir(resSinglePath):
        if ProjectPath.find("trunk") >  -1:
            url = "https://192.168.40.221:8833/svn/mlrelease2017/trunk/res_single"
        else:
            url = "https://192.168.40.221:8833/svn/mlrelease2017/branches/res_single/Android-%s" % (ver)
        SvnUtil.Svn_Checkout(url, resSinglePath)
        
    cmd = "%s -quit -projectPath %s -logfile %s -buildTarget %s -batchmode -executeMethod ExportAssetBundle.%s assetFile-%s platform-%s" % (UnityPath, ProjectPath, BuildLogFile, target, usingFunc, rawFile, platform)
    Util.RunCmd(cmd)

    ver = ReadLastSvnCollectVersion(ProjectPath, platform)
    WriteLastSvnVersion(ProjectPath, ver, platform)

    SvnDelAllFiles(ProjectPath, platform)
    SvnUtil.Svn_Add_Force(resSinglePath)
    SvnUtil.Svn_Commit(resSinglePath, svnComment)

   
#################################################################################

if __name__ == '__main__':
    code = 0
    try:
        before = Util.BeginTime_Sec("build_single_res")
        Main()
        Util.EndTime_Sec(before, "build_single_res")
    except Exception as e:
        code = 1
        print("!EXCEPTION!", e)
        traceback.print_exc()
    finally:
        print("-- build_single_res.py end --")
    
    sys.exit(code)
            