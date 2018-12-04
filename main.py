# -*- coding: utf-8 -*-

import tkinter
from tkinter import ttk

rootWindow = tkinter.Tk()
rootWindow.title('编辑服务器')
rootWindow.geometry('430x300')
rootWindow.resizable(False, False)

label_svrList = tkinter.Label(rootWindow, text = '服务器列表')
label_svrList.place(x = 10, y = 20, width = 80, height = 20)

listbox_svrList = tkinter.Listbox(rootWindow)
listbox_svrList.place(x = 10, y = 40, width = 170, height = 165)

button_addSvr = tkinter.Button(rootWindow, text = '添加(A)')
button_addSvr.place(x = 10, y = 220, width = 80, height = 25)

button_delSvr = tkinter.Button(rootWindow, text = '删除(D)')
button_delSvr.place(x = 100, y = 220, width = 80, height = 25)

button_cpySvr = tkinter.Button(rootWindow, text = '复制(C)')
button_cpySvr.place(x = 10, y = 250, width = 80, height = 25)

label_svrIP = tkinter.Label(rootWindow, text = '服务器地址')
label_svrIP.place(x = 185, y = 30, width = 80, height = 20)

entry_svrIP = tkinter.Entry(rootWindow)
entry_svrIP.place(x = 265, y = 30, width = 140, height = 20)

label_svrPort = tkinter.Label(rootWindow, text = '服务器端口')
label_svrPort.place(x = 185, y = 60, width = 80, height = 20)

entry_svrPort = tkinter.Entry(rootWindow)
entry_svrPort.place(x = 265, y = 60, width = 140, height = 20)

label_svrPass = tkinter.Label(rootWindow, text = '密码')
label_svrPass.place(x = 185, y = 90, width = 80, height = 20)

entry_svrPass = tkinter.Entry(rootWindow, show = '*')
entry_svrPass.place(x = 265, y = 90, width = 140, height = 20)

PPshow = tkinter.IntVar()
def showPassword():
    if PPshow.get() == 0:
        entry_svrPass.config(show = '*')
    else:
        entry_svrPass.config(show = '')

CekBtn_showPass = tkinter.Checkbutton(rootWindow, text = '显示密码',
                    variable = PPshow, command = showPassword)
CekBtn_showPass.place(x = 260, y = 120, height = 20)

label_encrpMethod = tkinter.Label(rootWindow, text = '加密方式')
label_encrpMethod.place(x = 185, y = 150, width = 80, height = 20)

combox_encrpMethod = ttk.Combobox(rootWindow)
combox_encrpMethod.place(x = 265, y = 150, width = 140, height = 20)

label_svrRmk = tkinter.Label(rootWindow, text = '备注名称')
label_svrRmk.place(x = 185, y = 180, width = 80, height = 20)

entry_svrRmk = tkinter.Entry(rootWindow)
entry_svrRmk.place(x = 265, y = 180, width = 140, height = 20)

label_ProxyPort = tkinter.Label(rootWindow, text = '代理端口')
label_ProxyPort.place(x = 185, y = 210, width = 80, height = 20)

entry_ProxyPort = tkinter.Entry(rootWindow)
entry_ProxyPort.place(x = 265, y = 210, width = 140, height = 20)


rootWindow.mainloop()