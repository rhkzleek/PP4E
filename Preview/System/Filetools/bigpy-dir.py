#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/24 19:18
#fileName:bigpy-dir.py.py
#tool:PyCharm


"""
TODO：找出单个目录下最大的Python 源代码文件
搜索Windows Python源代码库,除非指定了dir命令行参数
"""

import os, glob, sys

dirname = r'D:\GitHub\PP4E\Preview' if len(sys.argv) == 1 else sys.argv[1]

allsizes = []

allpy = glob.glob(dirname + os.sep + '*.py')

for filename in allpy:
    filesize = os.path.getsize(filename)
    allsizes.append((filesize, filename))

allsizes.sort()
print(allsizes)
print(allsizes[:2])
print(allsizes[-2:])
