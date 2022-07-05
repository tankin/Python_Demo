# -*- coding: utf-8 -*-
import configparser

def ReadConfig(configName):
    cf = configparser.ConfigParser()
    cf.read(configName)

    unity = cf.get('base', 'unity')
    projPath = cf.get("base", "projPath")
    return unity, projPath


unity, projPath = ReadConfig("CheckoutConfig.ini")
print(unity, projPath)