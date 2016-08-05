#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import sys

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5000 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

s.listen(10)
print 'Socket now listening'

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    print "waiting accept.."
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    while 1:
        data = conn.recv(1024)
        print "data:", data
        if not data: 
            break
        conn.sendall(data.upper())

    conn.close()
    print 'close connetion with ' + addr[0] + ':' + str(addr[1])

#关掉监听socket
s.close()
