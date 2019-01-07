#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2019/1/7 19:15
#fileName:config-label.py
#tool:PyCharm


from tkinter import *

root = Tk()
labelfont = ("times", 20, "bold")       #字体系列,大小,类型
widget = Label(root, text="Hello config world")
widget.config(bg="black", fg="yellow")      #在黑色标签上显示黄色2文本
widget.config(font=labelfont)                 #使用更大的字体
widget.config(height=3,width=20)              #初始化大小,行间距,字间距
widget.pack(expand=YES, fill=BOTH)

butWidget = Button(root, text='Spam',padx=10,pady=10)
butWidget.pack(padx=20,pady=20)
butWidget.config(cursor="gumby")
butWidget.config(bd=8, relief=RAISED)
butWidget.config(bg="dark green", fg="white")
butWidget.config(font=("helvetica",20, "underline italic"))
root.mainloop()

