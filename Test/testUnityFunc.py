# -*- coding: UTF-8 -*-
import os
import time

before = time.perf_counter()

UnityPath = "\"F:/Unity2021/Unity 2021.3.4f1/Editor/Unity.exe\""
ProjectPath = "F:/mygame_1.0.0.0.1"
BuildLogFile = "F:/t1.log"

csFunc = "ExportXlsx2CSV.OnExport"

cmd = "%s -quit -projectPath %s -logfile %s -batchmode -executeMethod %s" % (UnityPath, ProjectPath, BuildLogFile, csFunc)
#compress
#cmd = "%s -quit -projectPath %s -logfile %s -buildTarget Android -batchmode -executeMethod ExportAssetBundle.%s singleasset-%s" % (UnityPath, ProjectPath, BuildLogFile, usingFunc, rawFile)
os.system(cmd)


after = time.perf_counter()
print(after - before)