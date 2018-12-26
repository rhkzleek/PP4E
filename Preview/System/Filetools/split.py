#!/usr/bin/env python 
# -*- coding:utf-8 -*-



"""
TODO:将文件分割成很多组分,join.py将它们合并回去;
这是标准的Unix split命令行工具的一个可定制版本,因为它用Python写成,
所以在Windows下也能工作和方便的修改,因为它输出一个函数,所以它的逻辑业务也可以由其他应用程序导入并重复使用
"""

import sys, os
kilobytes = 1024
megabytes = kilobytes * 1000
chunksize = int(1.4 * megabytes)                #默认设置：大约一个软盘的容量


def split(fromfile, todir, chunksize = chunksize):
    if not os.path.exists(todir):               #调用者负责处理错误
        os.mkdir(todir)                          #创建目录,读写组分文件
    else:
        for fname in os.listdir(todir):         #删除任意已有文件
            os.remove(os.path.join(todir,fname))
    partnum = 0
    input2 = open(fromfile, 'rb')                #二进制模式:不解码，没有行尾
    while True:                                #行尾=从read得到空字符串
        chunk = input2.read(chunksize)           #获取下一个组分文件,大小<= chunksize
        if not chunk:
            break
        partnum +=1
        filename = os.path.join(todir, ('part%04d' %partnum))
        fileobj = open(filename, 'wb')
        fileobj.write(chunk)
        fileobj.close()
    input2.close()
    assert partnum <= 9999                      #待链接的文件超过9999个则不能执行
    return partnum


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-help':
        print('Use: split.py [file-to-split target-dir [chunksize]]')
    else:
        if len(sys.argv) < 3:
            interactive = True
            fromfile = input('File to be split?')               #如果单击运行脚本则要求输入
            todir = input('Directory to store part files?')
        else:
            interactive = False
            fromfile,todir = sys.argv[1:3]                         #命令行里的参数
            if len(sys.argv) == 4:
                chunksize = int(sys.argv[3])

        absfrom, absto = map(os.path.abspath, [fromfile,todir])
        print('Splitting', absfrom, 'to', absto, 'by', chunksize)


        try:
            parts = split(fromfile, todir, chunksize)
        except:
            print('Error during split:')
            print(sys.exc_info()[0], sys.exc_info()[1])
        else:
            print('Split finished:', parts, 'parts are in', absto)
        if interactive:
            input('Press Enter key')                        #如果单击运行脚本在此暂停
