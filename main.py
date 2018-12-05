# -*- coding: utf-8 -*-

import tkinter
import tkinter.messagebox
import json
import re
import os.path
from random import randint
from tkinter import ttk

if os.path.exists('./svrcfg.json') == False:
    with open("./svrcfg.json", 'w', encoding = 'utf-8') as fp:
        list_localsvr = [{'svrIP':'192.168.1.1', 'svrPort':'8080', 'svrPass':'123456', 
                    'encrpMethod':'chacha256', 'svrRmk':'Local'}]
        json.dump(list_localsvr, fp)

with open("./svrcfg.json", encoding = 'utf-8') as fp:
    dict_svrs = json.load(fp)

PPshow = tkinter.IntVar
encrpMethod = tkinter.StringVar

rootWindow = tkinter.Tk()
label_svrList = tkinter.Label(rootWindow)
listbox_svrList = tkinter.Listbox(rootWindow)
button_addSvr = tkinter.Button(rootWindow)
button_delSvr = tkinter.Button(rootWindow)
button_connSvr = tkinter.Button(rootWindow)
label_svrIP = tkinter.Label(rootWindow)
entry_svrIP = tkinter.Entry(rootWindow)
label_svrPort = tkinter.Label(rootWindow)
entry_svrPort = tkinter.Entry(rootWindow)
label_svrPass = tkinter.Label(rootWindow)
entry_svrPass = tkinter.Entry(rootWindow)
CekBtn_showPass = tkinter.Checkbutton(rootWindow)
label_encrpMethod = tkinter.Label(rootWindow)
combox_encrpMethod = ttk.Combobox(rootWindow)
label_svrRmk = tkinter.Label(rootWindow)
entry_svrRmk = tkinter.Entry(rootWindow)
label_ProxyPort = tkinter.Label(rootWindow)
entry_ProxyPort = tkinter.Entry(rootWindow)


def writeCfg():
    with open('./svrcfg.json', 'w', encoding = 'utf-8') as wfp:
        json.dump(dict_svrs, wfp)

def refreshsvrList():
    listbox_svrList.delete(0, 'end')
    for dict_svr in dict_svrs:
        if dict_svr['svrRmk'] == '':
            listbox_svrList.insert('end', dict_svr['svrIP'])
        else:
            listbox_svrList.insert('end', dict_svr['svrRmk'])

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

    dict_curSvr = {'svrIP':svrIP, 'svrPort':svrPort, 'svrPass':svrPass,
                  'encrpMethod':str(encrpMethod), 'svrRmk':svrRmk}

    for dict_svrincfg in dict_svrs:
        if dict_svrincfg['svrIP'] == dict_curSvr['svrIP']:
            tkinter.messagebox.showwarning(title = 'ERROR',
                        message = 'This IP is already in your list')
            return
    
    dict_svrs.append(dict_curSvr)
    writeCfg()
    refreshsvrList()

def delSvr():
    curidx = int(listbox_svrList.curselection()[0])
    dict_svrs.pop(curidx)
    writeCfg()
    refreshsvrList()

def showPassword():
    if PPshow.get() == 0:
        entry_svrPass.config(show = '*')
    else:
        entry_svrPass.config(show = '')

def selectEncrpMethod():
    encrpMethod = combox_encrpMethod.get()

def initWindow():
    rootWindow.title('编辑服务器')
    rootWindow.geometry('440x300')
    rootWindow.resizable(False, False)

    label_svrList.config(text = '服务器列表')
    label_svrList.place(x = 10, y = 20, width = 80, height = 20)
    refreshsvrList()

    listbox_svrList.place(x = 10, y = 40, width = 170, height = 165)

    button_addSvr.config(text = '添加(A)', command = addSvr)
    button_addSvr.place(x = 10, y = 220, width = 80, height = 25)

    button_delSvr.config(text = '删除(D)', command = delSvr)
    button_delSvr.place(x = 100, y = 220, width = 80, height = 25)

    button_connSvr.config(text = '复制(C)')
    button_connSvr.place(x = 10, y = 250, width = 80, height = 25)

    label_svrIP.config(text = '*服务器地址')
    label_svrIP.place(x = 185, y = 30, width = 80, height = 20)

    entry_svrIP.place(x = 265, y = 30, width = 165, height = 20)

    label_svrPort.config(text = '*服务器端口')
    label_svrPort.place(x = 185, y = 60, width = 80, height = 20)

    entry_svrPort.place(x = 265, y = 60, width = 165, height = 20)

    label_svrPass.config(text = '*密码')
    label_svrPass.place(x = 185, y = 90, width = 80, height = 20)

    entry_svrPass.config(show = '*')
    entry_svrPass.place(x = 265, y = 90, width = 165, height = 20)

    CekBtn_showPass.config(text = '显示密码', variable = PPshow, 
                           command = showPassword)
    CekBtn_showPass.place(x = 260, y = 120, height = 20)

    label_encrpMethod.config(text = '*加密方式')
    label_encrpMethod.place(x = 185, y = 150, width = 80, height = 20)

    combox_encrpMethod.config(textvariable = encrpMethod)
    combox_encrpMethod.place(x = 265, y = 150, width = 165, height = 20)
    combox_encrpMethod.bind("<<ComboboxSelected>>", selectEncrpMethod)
    combox_encrpMethod['values'] = ('aes-256-cfb', 'aes-128-cfb',
                                    'chacha20', 'chacha20-ietf',
                                    'aes-256-gcm', 'aes-128-gcm',
                                    'chacha20-poly1305', 
                                    'chacha20-ietf-poly1305')
    combox_encrpMethod.current(7)

    label_svrRmk.config(text = '备注名称')
    label_svrRmk.place(x = 185, y = 180, width = 80, height = 20)

    entry_svrRmk.place(x = 265, y = 180, width = 165, height = 20)

    label_ProxyPort.config(text = '代理端口')
    label_ProxyPort.place(x = 185, y = 210, width = 80, height = 20)

    entry_ProxyPort.place(x = 265, y = 210, width = 165, height = 20)


initWindow()

rootWindow.mainloop()
