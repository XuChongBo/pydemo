#!usr/bin/env/ python
#-*-coding:utf-8-*-
from __future__ import print_function
import sys
import sys
# references:
#https://pymotw.com/2/sys/tracing.html
# http://www.dalkescientific.com/writings/diary/archive/2005/04/20/tracing_python_code.html
# https://docs.python.org/2/library/inspect.html
def h(x):
    return x+1

def f(x):
    x = h(x)
    return x+2
def g(x, a=1):
    print('in g')
    print('init x:', x)
    t = x+a
    x = t
    print('after x:', x)
    return t
def main():
    """
    print "In main"
    for i in range(5):
        print i, i*3
    print "Done."
    y3 = h(y2)
    """
    x = 0
    s = 1.0
    y1 = g(f(g(x, 4)), 6)
    y2 = g(f(f(y1)))

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        #卷积层
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)  #输入是 1  通道  输出是10通道   内核是5*5
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()  #随机选择输入的信道  将其设为 0
        #全连接层
        self.fc1 = nn.Linear(320, 50)  #输入向量的大小为320 输出向量的大小为 50
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))  #激活函数
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x)



"""
print main
print __file__
"""
def traceit(frame, event, arg):
    print(event)
    if event == "return":
        lineno = frame.f_lineno
        print('=====%s return  lineno %s ============' % (frame.f_code.co_name, lineno))
        print(frame.f_locals)             #当前层的函数参数 
        print("-************************--")
        print(frame.f_code.co_varnames)   #输出当前层的变量名
        for var in frame.f_code.co_varnames:
            if var in frame.f_locals:
                print(var, '->', frame.f_locals[var])
        print("last frame:",frame.f_back.f_code.co_name) #当前层的上一层的名字
        print(event,frame.f_code.co_name, frame.f_code, frame, frame.f_back)  #事件  当前层的名称   当前层的对象位置  上一层的对象位置
        print("-************************--")

    if event == "line":
        lineno = frame.f_lineno
        #print "line", lineno
    elif event == 'call': 
#elif event == 'call' and frame.f_back and frame.f_back.f_code.co_name == 'forward' and frame.f_back.f_code.co_filename == __file__:
        lineno = frame.f_lineno
        print('=====%s call lineno %s ============' % (frame.f_code.co_name, lineno))
        print(frame.f_locals)             #当前层的函数参数 
        print("-------------------------------------------------------")
        print(frame.f_code.co_varnames)   #输出当前层的变量名
        for var in frame.f_code.co_varnames:
            if var in frame.f_locals:
                print(var, '->', frame.f_locals[var])
        print("last frame:",frame.f_back.f_code.co_name) #当前层的上一层的名字
        print("-------------------------------------------------------")
        print(event,frame.f_code.co_name, frame.f_code, frame, frame.f_back)  #事件  当前层的名称   当前层的对象位置  上一层的对象位置
    return traceit


sys.settrace(traceit)
main()
sys.settrace(None)
print("-------------ok")
