import os
in_file = '../../data/cv_data/empire.jpg'
print in_file
print os.path.splitext(in_file)[0]+'.png'
print os.path.abspath(in_file)
print 'dirname: ', os.path.dirname(in_file)
print os.path.dirname(os.path.abspath(in_file))
print os.path.dirname('/Users/xcbfreedom/projects/data/aab.xx')
print 'basename:',os.path.basename('/Users/xcbfreedom/projects/data/aab.xx')
print os.path.splitext(os.path.basename('/Users/xcbfreedom/projects/data/aab.xx'))
print os.path.splitext(os.path.basename('/Users/xcbfreedom/projects/data/aab'))
print os.path.join('./data/xx_dir','a.txt')

from urlparse import urlparse
from os.path import splitext, basename

picture_page = "http://a.com/b/c/da4ca3509a7b11e19e4a12313813ffc0_7.jpg"
disassembled = urlparse(picture_page)
print disassembled.path 
print basename(disassembled.path)
filename, file_ext = splitext(basename(disassembled.path))
print filename
print file_ext 
