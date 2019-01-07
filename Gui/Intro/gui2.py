#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/30 16:26
#fileName:gui2.py
#tool:PyCharm


import sys
from tkinter import *

widget = Button(None, text='Hello widget world!',command=sys.exit)
widget.pack(side=LEFT)
print('*'*40)
widget.mainloop()