#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/29 18:03
#fileName:playfile.py
#tool:PyCharm

'''
TODO：尝试打开任意一种媒体文件，总是通过网页浏览器架构,不过也可以使用特定的播放器
代码不经过修改，有可能在你的系统上无法正常工作,对于音频文件,在Unix使用的filter
和命令行打开，在windows下利用文件名关联通过start命令打开(也就是说，使用你的机器打开文件,
有可能是音频播放器，也可能是一个网页浏览器),可以根据需要进行配置和扩展
playknownfile假定找到打开文件的媒体类型,而playfile尝试利用Pythonmimetypes模块自动决定媒体类型
碰到未知的mimetype或系统平台时,二者都尝试用python webbrower模块启动一个网页浏览器
'''

import os, sys, mimetypes, webbrowser

helpmsg = """
Sorry: can't find a media player for '%s' on your sysem!
Add an entry for your system to the media player dictionary
for this type of file in playfile.py, or play the file manually
"""

def trace(*args):           #用空格隔开
    print(*args)

#######################################
#播放器技巧: 通用或特定,待扩展
#######################################


class MediaTool:
    def __init__(self, runtext=''):
        self.runtext = runtext

    def run(self, mediafile, **options):            #多数情况下将忽略options
        fullpath = os.path.abspath(mediafile)       #当前工作目录可以是任何路径
        self.open(fullpath,**options)

class Filter(MediaTool):
    def open(self, mediafile, **ignored):
        media = open(mediafile, 'rb')
        player = os.popen(self.runtext, 'w')        #派生的shell工具
        player.write(media.read())                   #发送到它的stdin

class Cmdline(MediaTool):
    def open(self, mediafile, wait=False, **other): #运行任何命令行
        cmdline = self.runtext % mediafile
        os.system(cmdline)                           #用%s代表文件名

class Winstart(MediaTool):                          #使用Windows注册表
    def open(self, mediafile, wait = False, **other): #也可以使用os.system('start filee')
        if not wait:
            os.startfile(mediafile)
        else:
            os.system('start /WAIT ' + mediafile)

class Webbrower(MediaTool):
    #file:// 必须是绝对路径
    def open(self, mediafile, **options):
        webbrowser.open_new('file://%s' % mediafile, **options)

#######################################
# 媒体类型特异并且系统平台特异的策略:修改，或者传入一个新的策略作为代替
#######################################
#建立系统平台和播放器的对应关系:在此修改

audiotools = {
    'sunos5':Filter('/usr/bin/audioplay'),      #os.popen().write()
    'linux2':Cmdline('cat %s > /dev/audio'),    #至少在zaurus系统上是这样的
    'sunos4':Filter('/usr/demo/SOUND/play'),    #是的,就是这么老!
    'win32':Winstart()
    #'win32'：Cmdline('start %s')
}

videotools = {
    'linux2': Cmdline('tkcVideo_c700 %s'),       #zaurus pda
    'win32': Winstart()
}

imagetools = {
    'linux2': Cmdline('zimager %s'),            #zaurus pda
    'win32': Winstart()
}

texttools = {
    'linux2': Cmdline('vi %s'),                 #zaurus pda
    'win32': Cmdline('notepad %s')              #要不要试试PyEdit?
}

apptools = {
    'win32': Winstart()                         #doc,xls 等待
}

#建立文件名的mimetype和播放器表格的对应关系
mimetable = {
    'audio':audiotools,
    'video':videotools,
    'image':imagetools,
    'text':texttools,
    'application': apptools
}

#######################################
# 顶层接口
#######################################
def trywebbrowser(filename, helpmsg = helpmsg, **options):
    """
    用网页浏览器打开文本/html,另外对于其他文件类型,如果碰到未知的mimetype
    或系统平台,也用网页浏览器进行尝试,作为最后的办法
    :param helpmsg:
    :param options:
    :return:
    """
    trace('trying brower', filename)
    try:
        player = Webbrower() #在本地浏览器中打开
        player.run(filename, **options)
    except:
        print(helpmsg % filename) #否则没有打开的程序

def playknowfile(filename, playertable={}, **options):
    '''
    播放类已知的媒体文件:使用平台特异的播放器对象:如果这个平台下没有相应
    工具则派生一个网页浏览器:接收媒体特异的播放器表格
    :param playertable:
    :param options:
    :return:
    '''
    if sys.platform in playertable:
        playertable[sys.platform].run(filename,**options)       #特殊工具
    else:
        trywebbrowser(filename, **options)            #通用架构

def playfile(filename, mimetable=mimetable, **options):
    '''
    播放器任意类型媒体文件:使用mimetypes猜测媒体类型并对应到平台特异的播放器表格
    如果是文本/html，或者未知媒体类型,或者没有播放器表格,则派生网页浏览器
    :param filename:
    :param mimetable:
    :param options:
    :return:
    '''
    contenttype, encoding = mimetypes.guess_type(filename)      #检查名称
    if contenttype == None or encoding is not None:           #无法猜测
        contenttype = '?/?'                                     #可能是.txt.gz
    maintype, subtype = contenttype.split('/', 1)               #字符串格式: '图像/jpeg'
    if maintype == 'text' and subtype == 'html':
        trywebbrowser(filename, **options)                      #特例
    elif maintype in mimetable:
        playknowfile(filename, mimetable[maintype], **options)  #尝试使用播放器表格
    else:
        trywebbrowser(filename, **options)                      #其他类型

#######################################
# 自测代码
#######################################
if __name__ == '__main__':
    #playknowfile('sousa.au', audiotools,wait=True)
    #playknowfile('image.jpeg', imagetools,wait=True)
    #playknowfile('image.jpeg', imagetools)

    #媒体类型猜测完毕
    result = input('Stop players and press Enter')
    playfile(result)                    #图像/jpeg