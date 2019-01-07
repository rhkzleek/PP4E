#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/29 14:08
#fileName:find.py
#tool:PyCharm

"""
TODO：返回某个根目录及其子目录下所有匹配某个文件名模式的文件
已经停用标准库find模块的定制版本：以“PP4E.Tools.find”方式导入:和
原版类似,不过使用os.walk()循环,不支持修剪子目录,并且可作为顶层脚本运行

find()是一个生成器，利用os.walk()生成器产生匹配的文件名,可使用findlist()
强制生成结果列表
"""

import fnmatch, os

def find(pattern, startdir=os.curdir):
    for (thisdir, subsHere, filesHere) in os.walk(startdir):
        for name in subsHere + filesHere:
            if fnmatch.fnmatch(name, pattern):
                fullpath = os.path.join(thisdir, name)
                yield fullpath

def findlist(pattern, startdir=os.curdir, dosort=False):
    matches = list(find(pattern, startdir))
    if dosort:
        matches.sort()
    return matches

if __name__ == '__main__':
    import sys
    namepattern, startdir = sys.argv[1], sys.argv[2]
    for name in find(namepattern, startdir):
        print(name)