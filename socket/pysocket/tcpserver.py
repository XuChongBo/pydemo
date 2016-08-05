#!/usr/bin/env python
# -*- coding:utf-8 -*-
from SocketServer import TCPServer, ThreadingMixIn, StreamRequestHandler  

#定义支持多线程的服务类，注意是多继承  
class Server(ThreadingMixIn, TCPServer): 
    pass  

#定义请求处理类  
class Handler(StreamRequestHandler):
    def handle(self):  
        addr = self.request.getpeername()  
        print 'Got connection from ',addr  
        self.wfile.write('Thank you for connection')  

if __name__ == "__main__":
    server = Server(('', 1234), Handler)    #实例化服务类  
    server.serve_forever()  #开启服务  
