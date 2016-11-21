
# 

rfile.read(size) 会阻塞, 需要读到size大小的数据才会返回

recv(max_size)   会阻塞, 只要读到数据就可以返回, 若client端做close()则返回""


# send 和 wfile.write的区别

def mysend(self, msg):
    sent = 0
    while sent < len(msg):
        sent += self.socket.send(msg[sent:])

上面函数等价于 self.wfile.write(msg)

# 注意事项

1. listen(2) 可指定等待accept的请求队列的长度

2. listen_socket.settimeout    用指定accept的超时时间，即多久没有新连接进来则返回

3. client_socket.setttimeout   用指定连接上读数据时的阻塞时间

4. 对方close时 recv会获得空,  那server端如何判断 是对方close还是broken pipe?

# 待确认问题

broken pipe error 和 reset error

# 
#套在while中实现tcp长连接, 可以响应多次请求, 一旦一个请求出错,应该关掉连接,防止一错再错
while server.conn:
    try:
        msg = server.read_obj()
        logger.info("server: received: %s" % msg)
        start_time = time.time()
        server.speak2file(msg)
        print " cost:%s ms" % int((time.time()-start_time)*1000)
        server.send_obj(msg)
    #except socket.timeout as e:   # 这里应该把当前conn关掉，因为timeout可能是send_obj发生的, continue回去调用read_obj 则双方死锁. 
        #logger.debug("server: socket.timeout: %s" % e)
        #continue
    except ClinetClosedException as e:
        logger.info("server: %s" % e)
        server.close_connection()
        break
    except Exception as e:
        logger.error(traceback.format_exc())
        server.close_connection()
        break
