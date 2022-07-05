# -*- coding: utf-8 -*-


from Common import Util, SvnUtil
import traceback
import os


projPath = "f:\\mlproj2017"
assetPath = os.path.join(projPath, "Assets")
Util.RenameFile(assetPath, "GameEntry.cs", "GameEntry.csbak")
Util.CopyFileInSameDir(assetPath, "GameEntry.testAndPc", "GameEntry.cs")