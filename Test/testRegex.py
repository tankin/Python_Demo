# -*- coding: utf-8 -*-

import re


txt = "the rain in Spain"
comp = re.compile("\w+", re.I|re.DOTALL)

out = comp.match(txt)
out2 = comp.search(txt)
print(out)

dic = {"a":1, "b":2}
print("c" in dic)



# 将匹配的数字乘以 2
def double(matched):
    value = int(matched.group('value'))
    return str(value * 2)
 
s = 'A23G4HFD567'
print(re.sub('(?P<value>\d+)', double, s))

# 提选出文本中固定的信息
s = '1102231990xxxxxxxx'
res = re.search('(?P<province>\d{3})(?P<city>\d{3})(?P<born_year>\d{4})',s)
print(res.groupdict())


print(s[:-1])
