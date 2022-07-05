# -*- coding: utf-8 -*-

# python 安装的时候，没有勾选 add path
# svn安装的时候没有勾选cmd line，或者没有安装slik svn
# 1. 需要注意Unity运行路径、2. 是否有F盘或D盘、3. 磁盘空间是否有25G+


from Common import Util, SvnUtil
import traceback
import os
import configparser

#################################################################################
# platform: android, ios, windows
def UpdateAssets(path, platform):
    all = os.listdir(path)
    directories = [d for d in all if os.path.isdir(os.path.join(path, d))]
    for dir in directories:
        lowerDir = dir.lower()
        realPath = os.path.join(path, dir)
        if lowerDir == "art" or lowerDir == "ui" or lowerDir == "dragon":
            SvnUtil.Svn_Update_Depth(realPath, "empty")
        elif lowerDir == 'audio':
            platform = platform.lower()
            SvnUtil.Svn_Update_Depth(realPath, 'immediates')
            audioDirs = [d for d in os.listdir(realPath) if os.path.isdir(os.path.join(realPath,d))]
            for ad in audioDirs:
                if ad == platform:
                    SvnUtil.Svn_Update_Depth(os.path.join(realPath, ad), "infinity")
                else:
                    SvnUtil.Svn_Update_Depth(os.path.join(realPath, ad), "empty")
        else:            
            SvnUtil.Svn_Update_Depth(realPath, "infinity")


def UpdateTools(path):
    all = os.listdir(path)
    directories = [d for d in all if os.path.isdir(os.path.join(path, d))]
    for dir in directories:
        realPath = os.path.join(path, dir)
        if dir == "VersionUploaderProxy":
            SvnUtil.Svn_Update_Depth(realPath, "infinity")
        else:
            SvnUtil.Svn_Update_Depth(realPath, "empty")

def ModifyRealVersion(path, bTrunk):
    verPath = os.path.join(path, "version")
    androidPath = os.path.join(verPath, "android")
    realversionPath = os.path.join(androidPath, "realversion.xml")
    if bTrunk:
        with open(realversionPath, "w", encoding="UTF8") as f:
            lines = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<root realversion=\"1.1.12.100.1\"/>"
            f.write(lines)
        

def UpdateAssetsExternalLink(path, url, platform):
    bTrunk = url.find("trunk") >= 0
    platform = platform.capitalize() #Android, IOS, Windows
    AssetsPath = os.path.join(path, "Assets")
    streamingAssetsPath = os.path.join(AssetsPath, "StreamingAssets")

    externalLink = ["StreamingAssets %s" % (url)]
    SvnUtil.Svn_SetExternalLink(AssetsPath, externalLink)
    SvnUtil.Svn_Checkout_Depth(url, streamingAssetsPath, "immediates")
        
    all = os.listdir(streamingAssetsPath)
    directories = [d for d in all if os.path.isdir(os.path.join(streamingAssetsPath, d))]
    for dir in directories:
        if dir != ".svn" :
            if dir == "comlibs":
                SvnUtil.Svn_Update_Depth(os.path.join(streamingAssetsPath, dir), "empty")
            else:
                SvnUtil.Svn_Update_Depth(os.path.join(streamingAssetsPath, dir), "infinity")
    
    url = "https://192.168.40.221:8833/svn/mlrelease2017/trunk/StreamingAssets/Windows/AStarPath"
    SvnUtil.Svn_Checkout(url, os.path.join(streamingAssetsPath, "AStarPath"))

    ModifyRealVersion(streamingAssetsPath, bTrunk)


# platform :Android, iOS, Windows
def UpdateResSingle(path, url, platform):
    path = os.path.join(path, "res_single")
    SvnUtil.Svn_Checkout_Depth(url, path, "immediates")

    all = os.listdir(path)
    directories = [d for d in all if os.path.isdir(os.path.join(path, d))]
    for dir in directories:
        if dir != ".svn" :
            if dir == platform:
                SvnUtil.Svn_Update_Depth(os.path.join(path, dir), "infinity")
            else:
                SvnUtil.Svn_Update_Depth(os.path.join(path, dir), "empty")

def Job1(platform, projPath):
    # svn checkout --depth=immediates https://192.168.40.221:8833/svn/mlproj2017/branches/Android-1.6.52.713.1 f:\branch
    #url = "https://192.168.40.221:8833/svn/mlproj2017/branches/Android-%s" % (ver)    
    url = "https://192.168.40.221:8833/svn/mlproj2017/trunk"
    SvnUtil.Svn_Checkout_Depth(url, projPath, "immediates")

    all = os.listdir(projPath)
    arrInRoot = [d for d in all if os.path.isdir(os.path.join(projPath, d))]
    for dir in arrInRoot:
        if len(dir) > 0 and dir[0] != '.':
            assetPath = os.path.join(projPath, dir)
            if 'Assets' == dir :
                SvnUtil.Svn_Update_Depth(assetPath, "immediates")
                UpdateAssets(assetPath, platform)
            elif 'Doc' == dir : # or 'Tools' == dir
                SvnUtil.Svn_Update_Depth(assetPath, "empty")
            elif 'Tools' == dir:
                SvnUtil.Svn_Update_Depth(assetPath, "immediates")
                UpdateTools(assetPath)
            else:
                SvnUtil.Svn_Update_Depth(assetPath, "infinity")
    
    # external link
    #url = "https://192.168.40.221:8833/svn/mlrelease2017/branches/Android-%s/%s" % (ver, platform)
    url = "https://192.168.40.221:8833/svn/mlrelease2017/trunk/StreamingAssets/%s" % (platform)
    UpdateAssetsExternalLink(projPath, url, platform)


def Job2(platform, projPath, unity):
     # res_single
    #url = "https://192.168.40.221:8833/svn/mlrelease2017/branches/res_single/Android-%s" % (ver)
    url = "https://192.168.40.221:8833/svn/mlrelease2017/trunk/res_single"
    UpdateResSingle(projPath, url, platform)

    assetPath = os.path.join(projPath, "Assets")
    Util.RenameFile(assetPath, "GameEntry.cs", "GameEntry.csbak")
    Util.CopyFileInSameDir(assetPath, "GameEntry.testAndPc", "GameEntry.cs")
    Util.DelFile(os.path.join(projPath, "Assets/Scripts/MobaPlugin.dll"))

    #unity="C:\\Program Files\\Unity\\Editor\\Unity.exe"
    cmd = "\"%s\" -quit -projectPath %s -buildTarget Android -batchmode -executeMethod ExportAssetBundle.AutoUpdateBundle" % (unity, projPath)
    Util.RunCmd(cmd)

def ReadConfig(configName):
    cf = configparser.ConfigParser()
    cf.read(configName)

    unity = cf.get('base', 'unity')
    projPath = cf.get("base", "projPath")
    return unity, projPath


def Main():
    #argvs = Util.GetSysArg(1)
    #unityVer = argvs[0]
    #print(argvs)
    
    platform = "Android" #"Windows" #iOS, Android
    ver = "trunk" #"1.6.52.713.1"

    print("Platform: ", platform)
    print("Branch version: ", ver)
    
    unity="C:\\Unity\\Editor\\Unity.exe"
    projPath = "f:\\SimpleTrunk"
    unity, projPath = ReadConfig("CheckoutConfig.ini")
    #projPath = "D:\\SimpleTrunk"

    Job1(platform, projPath)
    Job2(platform, projPath, unity)
   
   
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