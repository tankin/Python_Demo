# -*- coding: UTF-8 -*-

import argparse
from ast import parse

parser = argparse.ArgumentParser(description='自动拉取分支')

#parser.add_argument('int', type=str, help='input the integer')
parser.add_argument('--family', type=str, help='last name')
parser.add_argument('--name', type=str, help='first name')
parser.add_argument("--platform", help=u"平台", type=str, choices=['windows', "android", "ios"], default="windows", required=True)

args = parser.parse_args()


#print(parser.description)
#print(args)
#print(args.int)
print(args.family, args.name)
