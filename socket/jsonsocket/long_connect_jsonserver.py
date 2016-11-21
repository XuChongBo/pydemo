#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import socket
import struct
import logging
import time

logger = logging.getLogger("jsocket")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)
    
   
class JsonServer(object):
    def __init__(self, address, port):
        self.address = address
        self.port = port 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print dir(self.socket)
        self.socket.bind( (self.address, self.port) )
        #socket.listen(10)
        self.socket.listen(1)
        self.timeout = 5
        self.socket.settimeout(self.timeout)   # here timeout is played on accept()
        self.conn = None
    
    
    def accept_connection(self):
        self.conn, addr = self.socket.accept()
        self.conn.settimeout(self.timeout)
        logger.debug("connection accepted, conn socket (%s,%d)" % (addr[0],addr[1]))


    def send_obj(self, obj):
        msg = json.dumps(obj)
        frmt = "=%ds" % len(msg)
        packed_msg = struct.pack(frmt, msg)
        packed_hdr = struct.pack('!I', len(packed_msg))
        
        self._send(packed_hdr)
        self._send(packed_msg)
            
    def _send(self, msg):
        sent = 0
        while sent < len(msg):
            sent += self.conn.send(msg[sent:])
            
    def _read(self, size):
        data = ''
        while len(data) < size:
            data_tmp = self.conn.recv(size-len(data))
            data += data_tmp
            if data_tmp == '':
                raise RuntimeError("socket connection broken")
        return data

    def _msg_length(self):
        d = self._read(4)
        s = struct.unpack('!I', d)
        return s[0]
    
    def read_obj(self):
        size = self._msg_length()
        data = self._read(size)
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return json.loads(msg[0])
    
    def close(self):
        self.socket.close()
        logger.debug("closing the listening socket")
            
    def close_connection(self):
        if self.conn:
            self.conn.close()
            logger.debug("closing the connection socket")
            self.conn = None
 

if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5100
    server = JsonServer(host, port)
    #now keep talking with the client
    try:
        while 1:
            #wait to accept a connection - blocking call
            print "waiting accept.."
            try:
                server.accept_connection()
            except socket.timeout as e:
                logger.debug("accept timeout: %s" % e)
                continue
            while 1:
                try:
                    msg = server.read_obj()
                    logger.info("server received: %s" % msg)
                    server.send_obj(msg)
                except Exception as e:
                    logger.error("server: %s" % e)
                    break
    finally:    
        server.close()
