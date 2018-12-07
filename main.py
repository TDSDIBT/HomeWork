# -*- coding: utf-8 -*-

import tkinter
import tkinter.messagebox
import socket
import logging
import json
import re
import os.path
from random import randint
from tkinter import ttk

rootWindow = tkinter.Tk()
label_svrList = tkinter.Label(rootWindow)
listbox_svrList = tkinter.Listbox(rootWindow)
button_addSvr = tkinter.Button(rootWindow)
button_delSvr = tkinter.Button(rootWindow)
button_connSvr = tkinter.Button(rootWindow)
button_disconnSvr = tkinter.Button(rootWindow)
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

int_PPshow = tkinter.IntVar()
tuple_selectedSvr = tuple()
list_svrs = list()
tuple_encrpMethods = ('aes-256-cfb', 
                'aes-128-cfb',
                'chacha20', 
                'chacha20-ietf',
                'aes-256-gcm', 
                'aes-128-gcm',
                'chacha20-poly1305',
                'chacha20-ietf-poly1305')

def writeCfg():
    with open('./svrcfg.json', 'w', encoding = 'utf-8') as wfp:
        json.dump(list_svrs, wfp)

def refreshsvrList():
    listbox_svrList.delete(0, 'end')
    for dict_svr in list_svrs:
        if dict_svr['svrRmk'] == '':
            listbox_svrList.insert('end', dict_svr['svrIP'])
        else:
            listbox_svrList.insert('end', dict_svr['svrRmk'])

def checkSelected():
    global tuple_selectedSvr
    tuple_selectedSvr = listbox_svrList.curselection()
    if not tuple_selectedSvr:
        tkinter.messagebox.showerror('ERROR', 'selected error')
        return False
    return True

def addSvr():
    svrIP = str(entry_svrIP.get())
    svrPort = str(entry_svrPort.get())
    svrPass = str(entry_svrPass.get())
    encrpMethod = str(combox_encrpMethod.get())
    svrRmk = str(entry_svrRmk.get())
    ProxyPort = str(entry_ProxyPort.get())

    if svrIP == '' or svrPass == '' or svrPort == '':
        tkinter.messagebox.showerror(title = 'ERROR', 
                        message = 'IP or Password or SeverPort is empty!')
        return

    if not re.match('^(\d){1,3}\.(\d){1,3}\.(\d){1,3}\.(\d){1,3}$', svrIP):
        tkinter.messagebox.showerror(title = 'ERROR',
                        message = 'Sever IP invalid!')
        return
    
    if not re.match('^(\d){1,5}$', svrPort):
        tkinter.messagebox.showerror(title = 'ERROR',
                        message = 'Sever Port invalid!')
        return

    dict_curSvr = {'svrIP':svrIP, 'svrPort':svrPort, 'svrPass':svrPass,
                  'encrpMethod':encrpMethod, 'svrRmk':svrRmk}

    for dict_svrincfg in list_svrs:
        if dict_svrincfg['svrIP'] == dict_curSvr['svrIP'] and \
           dict_svrincfg['svrPort'] == dict_curSvr['svrPort']:
            tkinter.messagebox.showwarning(title = 'ERROR',
                        message = 'This IP is already in your list')
            return
    
    list_svrs.append(dict_curSvr)
    writeCfg()
    refreshsvrList()

def delSvr():
    if checkSelected() == False:
        return

    curidx = int(tuple_selectedSvr[0])
    if list_svrs[curidx]['svrRmk'] == '':
        str_svrinfo = list_svrs[curidx]['svrIP']
    else:
        str_svrinfo = list_svrs[curidx]['svrRmk']
    
    res = tkinter.messagebox.askokcancel('', 
    'Do you want to delete the server '+str_svrinfo)
        
    if res == True:
        list_svrs.pop(curidx)
        writeCfg()
        refreshsvrList()

def connSvr():
    if checkSelected() == False:
        return
    
    curidx = int(tuple_selectedSvr[0])
    cursvrIP = list_svrs[curidx]['svrIP']
    cursvrPass = list_svrs[curidx]['svrPass']
    cursvrPort = list_svrs[curidx]['svrPort']
    cursvrEncrp = list_svrs[curidx]['encrpMethod']

    logging.error(msg = '1')

def disconnSvr():
    if checkSelected() == False:
        return
    
    curidx = int(tuple_selectedSvr[0])

def showPassword():
    if int_PPshow.get() == 0:
        entry_svrPass.config(show = '*')
    else:
        entry_svrPass.config(show = '')

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

    button_connSvr.config(text = '连接(C)', command = connSvr)
    button_connSvr.place(x = 10, y = 250, width = 80, height = 25)

    button_disconnSvr.config(text = '断开(D)', command = disconnSvr)
    button_disconnSvr.place(x = 100, y = 250, width = 80, height = 25)

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

    CekBtn_showPass.config(text = '显示密码', variable = int_PPshow, onvalue = 1, 
                           offvalue = 0, command = showPassword)
    CekBtn_showPass.place(x = 260, y = 120, height = 20)

    label_encrpMethod.config(text = '*加密方式')
    label_encrpMethod.place(x = 185, y = 150, width = 80, height = 20)

    combox_encrpMethod.place(x = 265, y = 150, width = 165, height = 20)
    combox_encrpMethod['values'] = tuple_encrpMethods
    combox_encrpMethod.current(0)

    label_svrRmk.config(text = '备注名称')
    label_svrRmk.place(x = 185, y = 180, width = 80, height = 20)

    entry_svrRmk.place(x = 265, y = 180, width = 165, height = 20)

    label_ProxyPort.config(text = '代理端口')
    label_ProxyPort.place(x = 185, y = 210, width = 80, height = 20)

    entry_ProxyPort.place(x = 265, y = 210, width = 165, height = 20)

def initCfg():
    global list_svrs
    if os.path.exists('./svrcfg.json') == False:
        with open("./svrcfg.json", 'w', encoding = 'utf-8') as fp:
            list_localtestsvr = [{'svrIP':'192.168.1.1', 
                                  'svrPort':'8080', 
                                  'svrPass':'123456', 
                                  'encrpMethod':'chacha256', 
                                  'svrRmk':'Local'}]
            json.dump(list_localtestsvr, fp)

    with open("./svrcfg.json", encoding = 'utf-8') as fp:
        list_svrs = json.load(fp)

    logging.basicConfig(
        filename = 'info.log',
        level = logging.DEBUG,
        format = '%(asctime)s [type:%(levelname)s] [line:%(lineno)d] %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S'
    )

initCfg()
initWindow()

rootWindow.mainloop()
