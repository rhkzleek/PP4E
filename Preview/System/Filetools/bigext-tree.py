#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/24 20:16
#fileName:bigext-tree.py
#tool:PyCharm

'''
TODO：找到任意目录树里所有给定类型的文件中最大的那个
避免重复路径,捕获错误,添加追踪和行数大小
同样使用集合,文件迭代器和生成器以避免装载整个文件
并试图绕过不可解码的目录/文件名称的打印
'''

import os, pprint
from sys import argv, exc_info

trace = 1 #0代表关闭 1代表目录 2代表加上文件
dirname, extname = os.curdir, '.py'     #默认为当前工作目录下的.py文件
if len(argv) > 1:
    dirname = argv[1]                   #例如: C:\,C:\python31\Lib
if len(argv) > 2:
    extname = argv[2]                   #例如: .pyw, .txt
if len(argv) > 3:
    trace = int(argv[3])

def tryprint(arg):
    try:
        print(arg)
    except UnicodeEncodeError:
        print(arg.encode())             #尝试原始字节字符串

visited = set()
allsizes = []
for (thisDir, subsHere, filesHere) in os.walk(dirname):
    if trace:
        tryprint(thisDir)
    thisDir = os.path.normpath(thisDir)
    fixname = os.path.normcase(thisDir)

    if fixname in visited:
        if trace:
            tryprint('skipping ',thisDir)
        else:
            visited.add(fixname)
            for filename in filesHere:
                if filename.endswith(extname):
                    if trace > 1:
                        tryprint('+++' + filename)
                    fullname = os.path.join(thisDir, filename)
                    try:
                        bytesize = os.path.getsize(fullname)
                        linesize = sum(+1 for line in open(fullname, 'rb'))
                    except Exception:
                        print('error ', exc_info()[0])
                    else:
                        allsizes.append((bytesize,linesize,fullname))


for (title, key) in [('bytes', 0), ('lines', 1)]:
    print('\nBy %s...' %title)
    allsizes.sort(key=lambda x: x[key])
    pprint.pprint(allsizes[:3])
    pprint.pprint(allsizes[-3:])

