#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/27 20:15
#fileName:diffall.py
#tool:PyCharm

'''
TODO：用法："python diffall.py dir1 dir2"
递归的目录树比较:报告仅在dir2而非dir2中存在特有文件,报告dir1和dir2
同名但内容不同的文件,报告dir1和dir2中同名但不同类型的情况,并对dir1和地热
下所有同名子目录及其目录进行相同操作,输出的末尾打印差异总结,不过
其中的细节请在重定向的输出中搜索DIFF和unique字符串,新特性
将大文件的读取限制在每次1MB
捕获文件和目录同名的情况
通过在这个版本里传入结果避免在dirdiff.comparedirs()中再次调用os.listdir()
'''

import os
from Preview.System.Filetools import dirdiff

blocksize = 1024 * 1024             #每次最多读取1MB

def intersect(seq1, seq2):
    """
    返回seq1和seq2中所有共有项
    也可以使用set(seq1) & set(seq2) 不过集合是随机顺序的
    可能失去任何依赖平台的目录顺序
    :param seq1:
    :param seq2:
    :return:
    """

def comparetrees(dir1, dir2, diffs, verbose = False):
    '''
    比较两个目录树中所有子目录和文件,使用二进制文件来阻止Unicode编码
    和换行转换,因为目录树可能含有二进制文件和文本文件,可能需要listdir
    的bytes参数来处理某些平台上不可解码的文件名
    :param dir1:
    :param dir2:
    :param dir3:
    :param verbose:
    :return:
    '''

    #比较文件名列表
    print('*'*20)
    name1 = os.listdir(dir1)
    name2 = os.listdir(dir2)

    if not dirdiff.comparedirs(dir1, dir2, name1, name2):
        diffs.append('unique files at %s - %s' %(dir1, dir2))

    print('Comparing contents')
    common = intersect(name1,name2)
    missed = common[:]

    #比较共有文件的内容
    for name in common:
        path1 = os.path.join(dir1, name)
        path2 = os.path.join(dir2, name)
        if os.path.isfile(path1) and os.path.isfile(path2):
            missed.remove(name)
            file1 = open(path1, 'rb')
            file2 = open(path2, 'rb')
            while True:
                bytes1 = file1.read(blocksize)
                bytes2 = file2.read(blocksize)
                if (not bytes1) and (not bytes2):
                    if verbose:
                        print(name, 'matches')
                        break
                if bytes1 != bytes2:
                    diffs.append('files differ at %s - %s '%(path1, path2))
                    print(name, 'DIFFERS')
                    break
    #递归比较共有目录
    for name in common:
        path1 = os.path.join(dir1,name)
        path2 = os.path.join(dir2, name)
        if os.path.isdir(path1) and os.path.isdir(path2):
            missed.remove(name)
            comparetrees(path1, path2, diffs, verbose)

    #同名但一个是文件,另外一个是目录
    for name in missed:
        diffs.append('files missed at %s -%s: %s' %(dir1, dir2, name))
        print(name, 'DIFFERS')

if __name__ == '__main__':
    dir1, dir2 = dirdiff.getargs()
    diffs = []
    comparetrees(dir1, dir2, dirdiff, True)             #原位修改差异
    print('='*40)                                       #遍历,报告差异列表
    if not diffs:
        print('No diffs found.')
    else:
        print('Diffs found：', len(diffs))
        for diff in diffs:
            print('-', diff)