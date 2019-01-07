#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/29 14:35
#fileName:search_all.py
#tool:PyCharm

'''
TODO:用法: python ... \Tools\search_all.py dir string
搜索指定的目录及其子目录下所有含有指定字符串的文件,首先利用os.walk()接口而不是
find.find来收集文件名:类似于对find.find搜索‘*’模式的每个返回结果调用visitfile
'''

import os, sys
listonly = False
textexts = ['.py', 'pyc', '.txt', '.c', '.h']    #忽略二进制文件

def searcher(startdir, searchkey):
    global fcount, vcount
    for (thisdir, dirsHere, filesHere) in os.walk(startdir):
        for fname in filesHere: #do non-dir files here
            fpath = os.path.join(thisdir, fname)    #fnames 不能带路径名
            visitfile(fpath, searchkey)

def visitfile(fpath, searchkey):            #对于每个非目录文件进行迭代
    global fcount, vcount                   #搜索字符串
    print(vcount + 1, '=>', fpath)          #跳过受保护的文件
    try:
        if not listonly:
            if os.path.spltext(fpath)[1] not in textexts:
                print('Skipping', fpath)
            elif searchkey in open(fpath).read():
                input('%s has %s' % (fpath, searchkey))
                fcount += 1
    except:
        print('Failed：', fpath, sys.exc_info()[0])
    vcount += 1

if __name__ == '__mmain__':
    searcher(sys.argv[1], sys.argv[2])
    print('Found in %d files, visited %d' %(fcount, vcount))
