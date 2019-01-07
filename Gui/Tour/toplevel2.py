#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2019/1/7 19:46
#fileName:toplevel2.py
#tool:PyCharm

"""
弹出三个新窗口,destroy()会停止一个窗口,quit()会停止所有窗口和程序(停止主循环)
顶层窗口有标题,图标,图标化/移除图标以及wm事件的协议;总是会有一个应用程序根窗口,
无论创建或者显式创建一个Tk()对象,所有顶层窗口都是容器,但是它们永远都不会被封装/
网格化
Toplevel就像Frame,但它是一个新窗口并且可以包含一个菜单
"""

from tkinter import *
root = Tk()                 #显式根窗口

trees = [("The Larch!", "light blue"),
         ("The Pine!","light green"),
         ("The Giant Redwood!", "red")]

for (tree, color) in trees:
    win = Toplevel(root)                        #新建窗口
    win.title("Sing...")                      #设置边框
    win.protocol("WM_DELETE_WINDOW", lambda :None)  #忽略关闭
    win.iconbitmap("image.jpeg")                    #非红色Tk

    msg = Button(win, text=tree, command=win.destroy)       #关闭一个win
    msg.pack(expand=YES, fill=BOTH)
    msg.config(padx=10, pady=10, bd=10, relief=RAISED)
    msg.config(bg="black", fg=color, font=("times", 30, "bold italic"))

root.title("Lumberjack demo")
Label(root, text="Main window", width=30).pack()
Button(root, text="Quit All", command=root.quit).pack()     #终止所有程序
root.mainloop()