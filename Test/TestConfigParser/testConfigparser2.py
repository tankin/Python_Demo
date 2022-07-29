import configparser
import os

os.chdir("D:\\Python_config")

cf = configparser.ConfigParser()

# add section / set option & key
cf.add_section("test")
cf.set("test", "count", 1)
cf.add_section("test1")
cf.set("test1", "name", "aaa")

# write to file
with open("test2.ini","w+") as f:
    cf.write(f)