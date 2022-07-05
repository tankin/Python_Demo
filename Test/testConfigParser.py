# -*- coding: utf-8 -*-

import configparser

cf = configparser.ConfigParser()
cf.read("f:\\python_test\\[db].txt")

secs = cf.sections()
print(secs, type(secs))

opts = cf.options("db")
print(opts, type(opts))

kvs = cf.items("db")
print(kvs, type(kvs))
print("db_host", kvs[2][0], kvs[2][1])

db_host = cf.get('db', 'db_host')
db_port = cf.getint("db", "db_port")
print(db_host, db_port)

