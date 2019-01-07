#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/29 15:35
#fileName:visitor.py
#tool:PyCharm

"""
TODO:测试：python ...\Tools\visit.py dir testmask [string] 使用类和子类
封装os.walk调用手法某些细节,以便进行遍历和搜索;testmask是一个整数比特掩码,每个可用的自我测试
占1位:另请参考：visitor_*/.py子类用例：框架中一般应当使用__X作为伪局部名称,
"""


import os, sys

class FileVisitor:
    '''
    访问startDir(默认位‘.’)下所有非目录文件:可通过重载visit*方法定制
    文件/目录处理器,情境参数/属性为可选子类特异的状态:追踪开关:0代表关闭
    1代表显示目录,2代表显示目录和文件
    '''
    def __init__(self, context=None, trace = 2):
        self.fcount = 0
        self.dcount = 0
        self.context = context
        self.trace = trace

    def run(self, startDir=os.curdir, reset=True):
        if reset:
            self.reset()
        for (thisDir, dirsHere, filesHere) in os.walk(startDir):
            self.visitfile(thisDir)
            for fname in filesHere:
                fpath = os.path.join(thisDir, fname)        #对非目录文件进行迭代
                                                            #fname不带路径
                self.visitfile(fpath)

    def reset(self):                                        #为了重复使用遍历器
        self.fcount = self.dcount = 0                       #为了相互独立的遍历操作

    def visitdir(self, dirpath):                            #called for each ddir
        self.dcount += 1                                    #待重写或扩展
        if self.trace > 0:
            print(dirpath, '...')

    def visitfile(self,filepath):                            #called for each file
        self.count += 1                                     #待重写或扩展
        if self.trace > 1:
            print(self.fcount, '=>', filepath)

class SearchVisitor(FileVisitor):
    '''
    在startDir及其子目录下的文件中搜索字符串:子类,根据需要重定义
    visitmatch，扩展列表和候选:子类可以使用testexts来指定进行搜索的文件
    类型(还可以重定义候选以对文本内容使用mimetypes)
    '''
    skipexts = []
    testtxts = ['.txt', '.py', '.pyw', '.html', '.c', '.h']         #搜索带有这些扩展名的文件
    #skipexts = ['.gif', '.jpg', '.pyc', '.o','.a', '.exe']          #或者跳过带有这些带有这些扩展名的文件


    def __init__(self, searchkey, trace=2):
        FileVisitor.__init__(self,searchkey,trace)
        self.scount = 0

    def reset(self):                        #进行相互独立的遍历时
        self.scount = 0

    def candidate(self, fname):             #重新定义mimetypes
        ext = os.path.splitext(fname)[1]
        if self.testtxts:
            return ext in self.testtxts    #在测试列表中
        else:
            return ext not in self.skipexts     #或者不在跳过列表中时

    def visitfile(self,fname):               #匹配测试
        FileVisitor.visitfile(self, fname)
        if not self.candidate(fname):
            if self.trace > 0:
                print('Skipping', fname)
        else:
            text = open(fname).read()        #如果不能解码则使用'rb'模式
            if self.context in text:
                self.visitmatch(fname, text)
                self.scount += 1

    def visitmatch(self, fname, text):      #处理一个匹配文件
        print('%s has %s' %(fname, self.context))       #在低一级水平重写

class EditVisitor(SearchVisitor):
    """
    编辑startDir及其子目录下含有字符串的文件
    """
    editor = r'C:\cygwin\bin\wim-nox.exe'   #计算机的编辑器，看具体机器

    def visitmatch(self, fname, text):
        os.system('%s %s'%(self.editor, fname))

import pprint

class LineByType(FileVisitor):
    srcExts = []  #在子类中定义

    def __init__(self, trace = 1):
        FileVisitor.__init__(self, trace=trace)
        self.srcLines = self.srcFiles = 0
        self.exSums = {ext:dict(files=0, lins=0) for  ext in self.srcExts}

    def visitsource(self, fpath, ext):
        if self.trace > 0:
            print(os.path.basename(fpath))
        lines = len(open(fpath, 'rb').readlines())
        self.srcFiles += 1
        self.srcLines += lines
        self.exSums[ext]['files'] += 1
        self.srcSum[ext]['lines'] += lines

    def visitfile(self,filepath):
        FileVisitor.visitfile(self, filepath)
        for ext in self.srcExts:
            if filepath.endswith(ext):
                self.visitsource(filepath, ext)
                break

class PyLines(LineByType):
    srcExts = ['.py', '.pyw']    #只有Python文件

from Preview.System.Filetools.cpall import copyfile
class CpallVisitor(FileVisitor):
    '''
    类似System\Filetools\cpall.py 不过是借助visitor类
    '''
    def __init__(self,fromDir, toDir, trace=True):
        self.fromDirLen = len(fromDir) + 1
        self.toDir = toDir
        FileVisitor.__init__(self, trace=trace)

    def visitdir(self, dirpath):
        toPath = os.path.join(self.toDir, dirpath[self.fromDirLen:])
        if self.trace:
            print('d', dirpath, '=>', toPath)
        os.mkdir(toPath)
        self.dcount += 1
    def visitfile(self,filepath):
        toPath = os.path.join(self.toDir, filepath[self.fromDirLen:])
        if self.trace:
            print('f', filepath, '=>', toPath)
            copyfile(filepath, toPath)
            self.fcount += 1


class SourceLines(LineByType):
    srcExts = ['.py', '.pyw', '.cgi', '.html', '.c', '.cxx', '.h', '.i']



class ReplaceVisitor(SearchVisitor):
    '''
    将startDir及其子目录下的所有文件中的fromStr替换为toStr：运行后，
    修改过的变量文件存储在列表obj.changed中
    '''

    def __init__(self,fromStr, toStr, listOnly=False, trace=0):
        self.changed = []
        self.toStr =toStr
        self.listOnly = listOnly
        SearchVisitor.__init__(self, fromStr, trace)

    def visitmatch(self,fname, text):
        self.changed.append(fname)
        if not self.listOnly:
            fromStr, toStr = self.context, self.toStr
            text = text.replace(fromStr, toStr)
            open(fname, 'w').write(text)



if __name__ == '__main__':  #自测逻辑业务
    dolist = 1
    dosearch = 2            #3=进行列出和搜索
    donext = 4              #添加了下一个测试时

    def selftest(testmark):
        if testmark & dolist:
            visitor = FileVisitor(trace=2)
            visitor.run(sys.argv[2])
            print('Visited %d files and %d dirs' %(visitor.fcount, visitor.dcount))

        if testmark & dosearch:
            visitor = SearchVisitor(sys.argv[3], trace=0)
            visitor.run(sys.argv[2])
            print('Found in %d files, visited %d' %(visitor.scount, visitor.fcount))

    selftest(int(sys.argv[1]))