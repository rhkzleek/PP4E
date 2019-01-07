#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/30 15:47
#fileName:guil.py
#tool:PyCharm


from tkinter import *
root = Tk()
widget = Label(root)
widget.config(text = 'Hello GUI world!')
#expand=YES 选项要求打包几何管理器为组件扩展空间,通常可以是父组件中任何未被占用的地方
#fill选项,可用来拉伸组件,使其充满分配的空间fill=Y垂直拉伸,fill=X水平拉伸
widget.pack(expand=YES,fill=BOTH,side=TOP)
root.title('guil.py')
root.mainloop()