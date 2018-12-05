# -*- coding: utf-8 -*-

import tkinter
import tkinter.messagebox
import json
import re
from random import randint
from tkinter import ttk

rootWindow = tkinter.Tk()
rootWindow.title('编辑服务器')
rootWindow.geometry('440x300')
rootWindow.resizable(False, False)

label_svrList = tkinter.Label(rootWindow, text = '服务器列表')
label_svrList.place(x = 10, y = 20, width = 80, height = 20)

listbox_svrList = tkinter.Listbox(rootWindow)
listbox_svrList.place(x = 10, y = 40, width = 170, height = 165)

def addSvr():
    svrIP = str(entry_svrIP.get())
    svrPort = str(entry_svrPort.get())
    svrPass = str(entry_svrPass.get())
    # encrpMethod
    svrRmk = str(entry_svrRmk.get())
    ProxyPort = str(entry_ProxyPort.get())

    if svrIP == '' or svrPass == '' or svrPort == '':
        tkinter.messagebox.showerror(title = 'ERROR', 
                        message = 'IP or Password or SeverPort is empty!')
        return

    if not re.match('^(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}$', svrIP):
        tkinter.messagebox.showerror(title = 'ERROR',
                        message = 'IP invalid!')
        return

    '''
    testdict = {'svrIP':'172.16.1.1', 'svrPort':'8080', 'svrPass':'abc123', 
                    'encrpMethod':'chacha256', 'svrRmk':'My first Sever'}

    with open("./svrcfg.json", "w") as f:
        json.dump(testdict, f)
    '''

    dict_curSvr = {'svrIP':svrIP, 'svrPort':svrPort, 'svrPass':svrPass,
                  'encrpMethod':str(encrpMethod), 'svrRmk':svrRmk}

    with open("./svrcfg.json", encoding = 'utf-8') as fp:
        dict_svrs = json.load(fp)
        for dict_svrincfg in dict_svrs:
            if dict_svrincfg['svrIP'] == dict_curSvr['svrIP']:
                tkinter.messagebox.showwarning(title = 'ERROR',
                            message = 'This IP is already in your list')
                return
        dict_svrs.append(dict_curSvr)
    
    with open('./svrcfg.json', 'w', encoding = 'utf-8') as wfp:
        json.dump(dict_svrs, fp)


button_addSvr = tkinter.Button(rootWindow, text = '添加(A)', 
                                            command = addSvr)
button_addSvr.place(x = 10, y = 220, width = 80, height = 25)

button_delSvr = tkinter.Button(rootWindow, text = '删除(D)')
button_delSvr.place(x = 100, y = 220, width = 80, height = 25)

button_cpySvr = tkinter.Button(rootWindow, text = '复制(C)')
button_cpySvr.place(x = 10, y = 250, width = 80, height = 25)

label_svrIP = tkinter.Label(rootWindow, text = '*服务器地址')
label_svrIP.place(x = 185, y = 30, width = 80, height = 20)

entry_svrIP = tkinter.Entry(rootWindow)
entry_svrIP.place(x = 265, y = 30, width = 165, height = 20)

label_svrPort = tkinter.Label(rootWindow, text = '*服务器端口')
label_svrPort.place(x = 185, y = 60, width = 80, height = 20)

entry_svrPort = tkinter.Entry(rootWindow)
entry_svrPort.place(x = 265, y = 60, width = 165, height = 20)

label_svrPass = tkinter.Label(rootWindow, text = '*密码')
label_svrPass.place(x = 185, y = 90, width = 80, height = 20)

entry_svrPass = tkinter.Entry(rootWindow, show = '*')
entry_svrPass.place(x = 265, y = 90, width = 165, height = 20)

PPshow = tkinter.IntVar()
def showPassword():
    if PPshow.get() == 0:
        entry_svrPass.config(show = '*')
    else:
        entry_svrPass.config(show = '')

CekBtn_showPass = tkinter.Checkbutton(rootWindow, text = '显示密码',
                    variable = PPshow, command = showPassword)
CekBtn_showPass.place(x = 260, y = 120, height = 20)

label_encrpMethod = tkinter.Label(rootWindow, text = '*加密方式')
label_encrpMethod.place(x = 185, y = 150, width = 80, height = 20)

def selectEncrpMethod():
    encrpMethod = combox_encrpMethod.get()

encrpMethod = tkinter.StringVar
combox_encrpMethod = ttk.Combobox(rootWindow, textvariable = encrpMethod)
combox_encrpMethod.place(x = 265, y = 150, width = 165, height = 20)
combox_encrpMethod.bind("<<ComboboxSelected>>", selectEncrpMethod)

combox_encrpMethod['values'] = ('aes-256-cfb', 'aes-128-cfb',
                                'chacha20', 'chacha20-ietf',
                                'aes-256-gcm', 'aes-128-gcm',
                                'chacha20-poly1305', 
                                'chacha20-ietf-poly1305')
# combox_encrpMethod['state'] = 'readonly'
combox_encrpMethod.current(7)

label_svrRmk = tkinter.Label(rootWindow, text = '备注名称')
label_svrRmk.place(x = 185, y = 180, width = 80, height = 20)

entry_svrRmk = tkinter.Entry(rootWindow)
entry_svrRmk.place(x = 265, y = 180, width = 165, height = 20)

label_ProxyPort = tkinter.Label(rootWindow, text = '代理端口',
                                textvariable = str(randint(1000, 64535)))
label_ProxyPort.place(x = 185, y = 210, width = 80, height = 20)

entry_ProxyPort = tkinter.Entry(rootWindow)
entry_ProxyPort.place(x = 265, y = 210, width = 165, height = 20)


rootWindow.mainloop()