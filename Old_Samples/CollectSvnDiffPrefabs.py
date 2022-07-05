# -*- coding: utf-8 -*-

from posixpath import relpath
from Common import Util, SvnUtil
import traceback
import os
import sys


#################################################################################

def ReadSvnVersion(projectPath, platform):
    svn_ver_path = os.path.join(projectPath, "res_single/%s/svn_ver.txt" % (platform))
    with open(svn_ver_path, "r", encoding="UTF-8") as f:
        last = f.readline()
        last = last.replace("\r\n", "")
        return last

def WriteCollectSvnVersion(projectPath, verNum, platform):
    svn_ver_path = os.path.join(projectPath, "res_single/%s/svn_ver_collect.txt" % (platform))
    with open(svn_ver_path, "w", encoding="UTF-8") as f:
        f.write(verNum)


def ReadDependInfo(projectPath, platform):
    dependInfoPath = os.path.join(projectPath, "res_single/%s/res_single_dependInfo.txt" % (platform))
    with open(dependInfoPath, "r", encoding="UTF-8") as f:
        cont = f.readlines()
        return cont

def ParseDependInfo(cont):
    dependInfo = []
    for line in cont:
        line = line.replace('\n', '')
        assets = line.split(',')
        dependInfo.append(assets)
    return dependInfo

def GetPrefabInDependInfo(dependInfo, changeOne):
    for assets in dependInfo:
        size = len(assets)
        for asset in range(1, size): #index 0, 是这个prefab资源本身
            if changeOne == asset:
                return assets[0]
    return ""

def CollectPrefabs(projectPath, changesInSvn, platform):
    cont = ReadDependInfo(projectPath, platform)
    dependInfo = ParseDependInfo(cont)
    result = []
    for one in changesInSvn:
        if one.lower().endswith(".prefab"):
            result.append(one)
        else:
            asset = GetPrefabInDependInfo(dependInfo, one)
            if asset != "" and not asset in result:
                result.append(asset)
    return result

def CollectSvnChangedAssets(projectPath, allLines):
    changeAssets = []
    deletePrefabs = []
    for line in allLines:
        if len(line) > 1 and not line.lower().endswith(".meta"):
            tag = line[0]
            pos = line.rfind("   ")
            line = line[pos + 3:]
            line = line.replace("\\", "/")
            line = line.replace(projectPath, "")

            if tag == 'M' or tag == 'A':
                if changeAssets.count(line) == 0:
                    changeAssets.append(line)
            if tag == 'D':
                if deletePrefabs.count(line) == 0:
                    deletePrefabs.append(line)

    return changeAssets, deletePrefabs


# import: update the list by the file existance, avoid some asset modified then deleted, or deleted then added back
def UpdateModifyPrefabsByExist(projectPath, prefabs):
    newPrefabs = []
    for asset in prefabs :
        path = os.path.join(projectPath, asset)
        if asset.lower().endswith('.prefab'):
            if os.path.isfile(path):
                newPrefabs.append(asset)
    return newPrefabs


def GetFileBaseNameWithoutExt(relPath):
    pos = relPath.rfind("/")
    pos2 = relPath.rfind(".prefab")
    baseNameWithoutExt = relPath[pos + 1 : pos2]
    return baseNameWithoutExt


def UpdateDeletePrefabsByExist(projectPath, prefabs, modifyPrefabs):
    newPrefabs = []
    for asset in prefabs :
        path = os.path.join(projectPath, asset)
        if asset.lower().endswith('.prefab'):
            if not os.path.isfile(path):
                newPrefabs.append(asset)    

    # if one prefab is deleted, and added in another place, or backwards action, we don't count it in
    modPrefabDic = []
    for modAsset in modifyPrefabs:
        modAssetBaseName = GetFileBaseNameWithoutExt(modAsset)
        modPrefabDic.append([modAssetBaseName, modAsset])
    
    finalPrefabs = []
    for newAsset in newPrefabs:
        realDel = True
        newAssetBaseName = GetFileBaseNameWithoutExt(newAsset)
        for unit in modPrefabDic:
            if unit[0] == newAssetBaseName:
                tmpPath = os.path.join(projectPath, unit[1])
                if os.path.isfile(tmpPath):
                    realDel = False
                    break
        if realDel:
            finalPrefabs.append(newAsset)

    return finalPrefabs

def WriteFileWithPrefabs(projectPath, prefabs, fileName):
    filePath = os.path.join(projectPath, fileName)
    with open(filePath, "w", encoding="UTF-8") as f:
        if len(prefabs) == 0:
            f.write("")
        else:
            firstLine = True
            for one in prefabs:
                if firstLine :
                    firstLine = False
                    f.write(one)
                else:
                    f.write("\n" + one)

def Main():
    argvs = Util.GetSysArg(2)
    ver = argvs[0]
    platform = argvs[1]
    print(argvs)
    
    #platform = "android"
    #projectPath = "F:/mlproj2017/"

    projectPath = "G:/autobuild/Android-%s/mobaclient-%s_singleRes_%s/" % (ver,ver, platform)
    print("projectPath: ", projectPath)

    artPath = os.path.join(projectPath, "Assets/Art")
    uiPath = os.path.join(projectPath, "Assets/UI")
    shaderPath = os.path.join(projectPath, "Assets/Shaders")    
    print("art path: ", artPath)
    print("ui path: ", uiPath)
    print("shader path:", shaderPath)

    last = ReadSvnVersion(projectPath, platform)
    print("last revision:", last)
    
    # -- Svn update --
    before = Util.BeginTime_Sec("SVN Update Art")
    SvnUtil.Svn_Update(artPath)
    Util.EndTime_Sec(before, "SVN Update Art")

    before = Util.BeginTime_Sec("SVN Update UI")
    SvnUtil.Svn_Update(uiPath)
    Util.EndTime_Sec(before, "SVN Update UI")

    before = Util.BeginTime_Sec("SVN Update Shader")
    SvnUtil.Svn_Update(shaderPath)
    Util.EndTime_Sec(before, "SVN Update Shader")

    # -- Art --
    curArt = SvnUtil.Svn_Info_Last_Changed_Revision_Old(artPath)
    print("cur art revision:", curArt)
    artList = []
    if last < curArt :
        allArt = SvnUtil.Svn_Diff(artPath, last, curArt)
        allArt = allArt.replace("\r", "")
        artList = allArt.split("\n")
    
    # -- UI --
    curUI = SvnUtil.Svn_Info_Last_Changed_Revision_Old(uiPath)
    print("cur ui revision:", curUI)
    UIList = []
    if last < curUI :
        allUI = SvnUtil.Svn_Diff(uiPath, last, curUI)
        allUI = allUI.replace("\r", "")
        UIList = allUI.split("\n")

    # -- shader --
    curShader = SvnUtil.Svn_Info_Last_Changed_Revision_Old(shaderPath)
    print("cur shader revision:", curShader)
    shaderList = []
    if last < curUI :
        allShader = SvnUtil.Svn_Diff(shaderPath, last, curShader)
        allShader = allShader.replace("\r", "")
        shaderList = allShader.split("\n")

    # -- total --
    allLines = artList + UIList + shaderList
    cur = max(curArt, curUI, curShader)
    print("artList %d, UIList %d, shaderList %d" % (len(artList), len(UIList), len(shaderList)))

    if len(allLines) > 0:
        changedAssets, deleteAssets = CollectSvnChangedAssets(projectPath, allLines)
        changedPrefabs = CollectPrefabs(projectPath, changedAssets, platform)
        changedPrefabs = UpdateModifyPrefabsByExist(projectPath, changedPrefabs)
        deletePrefabs  = UpdateDeletePrefabsByExist(projectPath, deleteAssets, changedPrefabs)
        WriteFileWithPrefabs(projectPath, changedPrefabs, "res_single_raw.txt")
        WriteFileWithPrefabs(projectPath, deletePrefabs, "res_single_del.txt")        
    else :
        WriteFileWithPrefabs(projectPath, [], "res_single_raw.txt")
        WriteFileWithPrefabs(projectPath, [], "res_single_del.txt")
        print("No action, last: %s, cur: %s" % (last, cur))

    WriteCollectSvnVersion(projectPath, cur, platform)
#################################################################################

if __name__ == '__main__':
    code = 0
    try:
        before = Util.BeginTime_Sec("CollectSvnDiffPrefabs")
        Main()
        Util.EndTime_Sec(before, "CollectSvnDiffPrefabs")
    except Exception as e:
        code = 1
        print("!EXCEPTION!", e)
        traceback.print_exc()
    finally:
        print("-- CollectSvnDiffPrefabs.py end --")
    
    sys.exit(code)
