# -*- coding: utf-8 -*-

from Common import Util, SvnUtil
import traceback
import os


#################################################################################

def Main():
    argvs = Util.GetSysArg(2)
    ver = argvs[0]
    assets = argvs[1]
    print(argvs)

    assets = assets.replace("\\", "/")
    assetList = str.split(assets, "#")

    rawFile = "res_single_raw.txt"
    ProjectPath = "G:/autobuild/Android-%s/mobaclient-%s" % (ver,ver)
    if not os.path.isdir(ProjectPath):
        print("[Error], dir not exist : %s" % (ProjectPath))
        return
    
    rawFilePath = os.path.join(ProjectPath, rawFile)
    with open(rawFilePath, "w", encoding='UTF-8') as f:
        f.writelines('\n'.join(assetList))

   
#################################################################################

if __name__ == '__main__':
    print("-- SaveResSingleRaw.py begin --")
    try:
        before = Util.BeginTime_Sec("SaveResSingleRaw")
        Main()
        Util.EndTime_Sec(before, "SaveResSingleRaw")
    except Exception as e:
        print("!EXCEPTION!", e)
        traceback.print_exc()
    finally:
        print("-- SaveResSingleRaw.py end --")