# -*- coding: utf-8 -*-


from Common import Util, SvnUtil
import traceback
import os


def UpdateTools(path):
    all = os.listdir(path)
    directories = [d for d in all if os.path.isdir(os.path.join(path, d))]
    for dir in directories:
        realPath = os.path.join(path, dir)
        if dir == "VersionUploaderProxy":
            SvnUtil.Svn_Update_Depth(realPath, "infinity")
        else:
            SvnUtil.Svn_Update_Depth(realPath, "empty")

assetPath = "f:\\SimpleTrunk\\Tools"
SvnUtil.Svn_Update_Depth(assetPath, "immediates")
UpdateTools(assetPath)

#SvnUtil.Svn_Update_Depth(assetPath, "empty")
#SvnUtil.Svn_Update_Depth(os.path.join(assetPath, "VersionUploaderProxy"), "infinity")