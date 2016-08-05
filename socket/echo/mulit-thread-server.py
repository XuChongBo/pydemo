#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import sys
from thread import *

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10) #带有一个参数称为 backlog，用来控制连接的个数。如果设为 10，那么有 10 个连接正在等待处理，此时第 11 个请求过来时将会被拒绝。
print 'Socket now listening'

#Function for handling connections. This will be used to create threads
def clientthread(conn,addr):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string

    #infinite loop so that function do not terminate and thread do not end.
    while True:
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
        conn.sendall(reply)

    #came out of loop
    conn.close()
    print 'close connection with ' + addr[0] + ':' + str(addr[1])

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])

    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,addr))

s.close()
