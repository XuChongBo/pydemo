"""
    open an image file and show it.
"""
from PIL import Image
from pylab import imshow,show,axis,ginput

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
imshow(img)
print 'Please click 3 points'
x = ginput(3)
print 'you clicked:',x 

show()

