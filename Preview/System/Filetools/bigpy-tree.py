#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/24 19:29
#fileName:bigpy-tree.py.py
#tool:PyCharm

'''
TODO:找出整个目录树中最大的python源代码文件
搜索Python源代码库,利用pprint漂亮的显示结果
'''

import sys,os, pprint
trace = False
if sys.platform[:3] == 'win':
    dirname = r'D:\GitHub\PP4E\Preview' #在window下可用
else:
    dirname = '/usr/lib/python'         #在Unix ， linux， Cygwin下可用

allsizes = []

for (thisDir, subsHere, filesHere) in os.walk(dirname):
    if trace:
        print(thisDir)
    for filename in filesHere:
        if trace:
            print('...', filename)
        fullname = os.path.join(thisDir, filename)
        fullsize = os.path.getsize(fullname)
        allsizes.append((fullsize, fullname))

allsizes.sort()
pprint.pprint(allsizes[:2])
pprint.pprint(allsizes[-2:])
pprint.pprint('*'*50)
pprint.pprint(allsizes)
