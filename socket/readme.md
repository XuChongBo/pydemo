
# 

rfile.read(size) 会阻塞, 需要读到size大小的数据才会返回

recv(max_size)   会阻塞, 只要读到数据就可以返回, 若client端做close()则返回""


# send 和 wfile.write的区别

def mysend(self, msg):
    sent = 0
    while sent < len(msg):
        sent += self.socket.send(msg[sent:])

上面函数等价于 self.wfile.write(msg)
