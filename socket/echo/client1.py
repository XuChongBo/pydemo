#!/usr/bin/env python
# -*- coding:utf-8 -*-

#Socket client example in python




import socket   #for sockets
import sys  #for exit
host = 'www.google.com'
port = 80

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Ip address of ' + host + ' is ' + remote_ip

try:
    #create an AF_INET, STREAM socket (TCP)
    #AF_INET（用于 Internet 进程间通信） 或者 AF_UNIX（用于同一台机器进程间通信）
    #SOCKET_STREAM（流式套接字，主要用于 TCP 协议）或者 SOCKET_DGRAM（数据报套接字，主要用于 UDP 协议）
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print 'Socket Created'

#Connect to remote server
s.connect((remote_ip , port))
print 'Socket Connected to ' + host + ' on ip ' + remote_ip

#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"
try :
    #Set the whole string
    #s.sendall(string[,flag])  将string中的数据发送到连接的套接字，但在返回之前会尝试发送所有数据。成功返回None，失败则抛出异常。
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()

print 'Message send successfully'

#Now receive data
#s.recv(bufsize[,flag])  接受套接字的数据。数据以字符串形式返回，bufsize指定要接收的最大数据量。flag提供有关消息的其他信息，通常可以忽略。
reply = s.recv(4096)
print reply

print "======= send again ======="
s.sendall(message)
print s.recv(4096)

#当我们不想再次请求服务器数据时，可以将该 socket 关闭，结束这次通信
s.close()
