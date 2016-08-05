#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
"""
Simple examples with StringIO module

类StringIO提供了一个在内存中方便处理文本的类文件(读, 写等操作)API. 

他有两个独立的实现, 
    一个是用c实现的cStringIO模块, 速度较快, 
    另一个是StringIO模块, 他用python实现的以增强其可移植性. 使用cStringIO来处理大字符串可以提高运行性能,优于其他字符串串联技术.
"""

# Find the best implementation available on this platform

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

# Writing to a buffer
output = StringIO()
output.write('This goes into the buffer. ')

print >>output, 'And so does this.'
# Retrieve the value written
print output.getvalue()

output.close() # discard buffer memory

# Initialize a read buffer
input = StringIO('Inital value for read buffer')

# Read from the buffer
print input.read()
