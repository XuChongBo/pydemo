#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
 
HOST= '0.0.0.0'     # 远程socket服务器ip
PORT= 5000          # 远程socket服务器端口
 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #实例化socket
s.connect((HOST,PORT))                               #连接socket服务器
 
while True:
    msg = raw_input("Your msg::").strip() #让用户输入消息，去除回车和空格
    if len(msg) == 0:
        continue 
    s.sendall(msg)           #向服务器发送消息
    data= s.recv(1024)       #接收服务器的消息
    print 'Received:', data

s.close()
