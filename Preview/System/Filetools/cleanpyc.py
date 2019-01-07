#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/29 14:24
#fileName:cleanpyc.py
#tool:PyCharm

"""
TODO：删除目录树中所有的.pyc字节码文件:如果给出命令行参数则将其作为根目录
否则将当前工作目录作为根目录
"""

import os,sys
findonly = False
rootdir = os.getcwd() if len(sys.argv) == 1 else sys.argv[1]

found = removed = 0
for (thisDirLevel, subsHere, fileHere) in os.walk(rootdir):
    for filename in fileHere:
        if filename.endswith('.pyc'):
            fullname = os.path.join(thisDirLevel, filename)
            print('=>', fullname)
            if not findonly:
                try:
                    os.remove(fullname)
                    removed += 1
                except:
                    type, inst = sys.exc_info()[:2]
                    print('*'*4, 'Failed:', filename, type, inst)

print('Found', found, 'files, removed', removed)