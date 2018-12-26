#!/usr/bin/env python 
# -*- coding:utf-8 -*-

"""
TODO:合并split。py创建的目录下的所有组分文件以重建文件
大概相当于Unix下的cat fromdir/* > tofile命令,不过可移植性和可配置性更好,
并且将合并操作作为可以重复使用的函数而输出,依赖文件名排序顺序：长度必须一致
可以进一步的扩展,分割/合并,弹出Tkinter文件选择器
"""

import sys,os
readsize = 1024

def join(fromdir, tofile):
    output = open(tofile, 'wb')
    parts = os.listdir(fromdir)
    parts.sort()
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj = open(filepath, 'rb')
        while True:
            filebytes = fileobj.read(readsize)
            if not filebytes:
                break
            output.write(filebytes)
        fileobj.close()
    output.close()

if __name__ in '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: join.py [from-dir-name to-file-name]')
    else:
        if len(sys.argv) != 3:
            interactive = True
            fromdir = input('Directory containing part files?')
            tofile = input('Name of file to be recreated?')
        else:
            interactive = False
            fromdir, tofile = sys.argv[1:]
        absfrom, absto = map(os.path.abspath, [fromdir, tofile])
        print('Joining', absfrom, 'to make', absto)

        try:
            join(fromdir, tofile)
        except:
            print('Error joining files:')
            print(sys.exc_info()[0], sys.exc_info()[1])
        else:
            print('Join complete: see', absto)

        if interactive:
            input('Press Enter key')
