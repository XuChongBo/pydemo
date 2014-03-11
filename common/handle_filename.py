import os
in_file = '../../data/cv_data/empire.jpg'
print in_file
print os.path.splitext(in_file)[0]+'.png'

print os.path.basename('/Users/xcbfreedom/projects/data/aab.xx')
print os.path.splitext(os.path.basename('/Users/xcbfreedom/projects/data/aab.xx'))
print os.path.splitext(os.path.basename('/Users/xcbfreedom/projects/data/aab'))
print os.path.join('./data/xx_dir','a.txt')
