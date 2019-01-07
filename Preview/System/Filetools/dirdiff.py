#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/27 19:56
#fileName:dirdiff.py
#tool:PyCharm


"""
TODO：用法 python dirdiff.py dir1-path dir-path
比较两个目录,找出其中一个目录中出现的文件
这个版本使用os.listdir函数并且吧差异汇总到列表,请注意这脚本只检文件
名而不涉及文件内容,关于后者的比较请参考diffall.py,它通过比较.read()
结果实现这方面功能的扩展
"""

import os,sys

def reportdiffs(unique1, unique2, dir1, dir2):
    """
    为目录生成差异报告,comparedirs函数输出一部分
    :param unique1:
    :param unique2:
    :param dir1:
    :param dir2:
    :return:
    """
    if not (unique1 or unique2):
        print('Directory lists are identical')
    else:
        if unique1:
            print('Files unique to', dir1)
            for file in unique1:
                print('...', file)
        if unique2:
            print('Files unique to', dir2)
            for file in unique2:
                print('...', file)

def difference(seq1, seq2):
    '''
    仅返回seq1中所有项
    也可以使用set(seq1) - set(seq2) 不过集合内的顺序是随机的,
    所以会导致失去具有平台依赖性的目录顺序
    :param seq1:
    :param seq2:
    :return:
    '''
    return [item for item in seq1 if item not in seq2]

def comparedirs(dir1, dir2, files1 = None, files2 = None):
    '''
    比较目录内容而非文件实际内容,可能需要listdir的bytes参数来处理
    :param dir1:
    :param dir2:
    :param files1:
    :param file2:
    :return:
    '''
    print('Comparing', dir1, 'to', dir2)
    files1 = os.listdir(dir1) if files1 is None else files1
    files2 = os.listdir(dir2) if files2 is None else files2
    unique1 = difference(files1, files2)
    unique2 = difference(files2, files1)
    reportdiffs(unique1, unique2,dir1, dir2)
    return not(unique1 or unique2)              #如果没有差别则为True

def getargs():
    '''
    命令行模式的参数
    :return:
    '''
    try:
        dir1, dir2 = sys.argv[1:]
    except:
        print('Usage: dirdiff.py dir1 dir2')
        sys.exit(1)
    else:
        return (dir1, dir2)


if __name__ == '__main__':
    dir1, dir2 = getargs()
    comparedirs(dir1, dir2)