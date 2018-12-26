#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/24 19:48
#fileName:bigpy-path.py
#tool:PyCharm

'''
TODO: 找出模块导入搜索路径下最大的python源代码文件,跳过已经访问的目录
统一路径和大小写格式以便使之正确匹配，并在pprint打印结果中添加文件行数
使用os.environ['PYTHONPATH']并不够,它只是sys.path的一个子集
'''

import sys, os, pprint
trace = 0 #1代表目录 2代表加上文件

visited = {}
allsizes = []

for srcdir in sys.path:
    for (thisDir, subsHere, filesHere) in os.walk(srcdir):
        if trace > 0:
            print(thisDir)
        thisDir = os.path.normpath(thisDir)
        fixcase = os.path.normcase(thisDir)
        if fixcase in visited:
            continue
        else:
            visited['fixcase'] = True
        for filename in filesHere:
            if filename.endswith('.py'):
                if trace > 1:
                    print('...', filename)
                pypath = os.path.join(thisDir,filename)
                try:
                    pysize = os.path.getsize(pypath)
                except os.error:
                    print('skipping', pypath, sys.exc_info()[0])
                else:
                    pylines = len(open(pypath, 'rb').readlines())
                allsizes.append((pysize,pylines,pypath))

print('By size...')
allsizes.sort()
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])

print('By lines...')
allsizes.sort(key=lambda x:x[1])
pprint.pprint(allsizes[:3])
pprint.pprint(allsizes[-3:])

