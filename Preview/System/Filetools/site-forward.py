#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
TODO:为迁移站点：创建转向链接页面
为每个已有的站点html文件生成一个页面:将生成的文件上传到你的旧网站.
关于在页面文件生成时或者之后在脚本中执行上传的方法，请参考ftblib
'''

import os
servername = 'learning-python.com'              #站点迁移的目的地
homedir = 'books'                                 #站点的根目录
sitefilesdir = r'C:\temp\public_html'           #站点文件在本地的路径
uploaddir = r'C:\temp\isp-forward'              #准备存放转向链接文件的目录
templatename = 'template.html'                   #待生成页面的模板

try:
    os.mkdir(uploaddir)                             #如有需要则创建上传目录
except OSError:
    pass

template = open(templatename).read()              #载入或导入模板文本
sitefiles = os.listdir(sitefilesdir)              #文件名,前面不带目录

count = 0
for filename in sitefiles:
    if filename.endswith('.html') or filename.endswith('.htm'):
        fwdname = os.path.join(uploaddir,filename)
        print('creating', filename, 'as', fwdname)
        filetext = template.replace('$server$', servername)         #插入文本
        filetext = filetext.replace('$home$', homedir)              #然后写入
        filetext = filetext.replace('$file$', filename)             #文件不同
        open(fwdname, 'w').write(filetext)
        count += 1

print('Last file =>\n', filetext,seq='')
print('Done:', count, 'forward files created')