#!/usr/bin/env python3
#-*- coding:utf-8 -*-
#auther:DELL
#createTime:2018/12/30 17:52
#fileName:gui5.py
#tool:PyCharm


from tkinter import *

class HelloButton(Button):
    def __init__(self, parent=None, **config):      #添加回调方法
        Button.__init__(self, parent, **config)      #把自己打包起来
        self.pack()
        self.config(command=self.callback)

    def callback(self):
        print('Goodbye world...')                  #默认为按下动作
        self.quit()


class MyButton(HelloButton):
    def callback(self):
        print('Ignoring press!...')

class ThemeButton(Button):
    def __init__(self, parent=None,**config):
        Button.__init__(self,parent, **config)
        self.pack()
        self.config(fg='red', bg='black', font=('courier',12),relief=RAISED, bd=10)

if __name__ == '__main__':
    #HelloButton(text='Hello subclass world',fg='red',bg='black',font=('courier', 12), relief=RAISED,bd=5).mainloop()
    B1 = ThemeButton(text='sqam', command=quit)
    B2 = ThemeButton(text='eggs')
    B2.pack(expand=YES, fill=BOTH)
    B2.mainloop()