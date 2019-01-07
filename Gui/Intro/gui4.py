#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/30 17:32
#fileName:gui4.py
#tool:PyCharm

from tkinter import *

def greeting():
    print('Hello stdout world!...')

win = Frame()
win.pack()


Button(win,text='Hello', command=greeting).pack(side=LEFT,anchor=N)

Label(win, text='Hello container world').pack(side=TOP)
Button(win,text='Quit', command=quit).pack(side=RIGHT)

win.mainloop()