from PIL import Image

from pylab import imshow,axis,contour,axis, figure,gray,hist,show
from numpy import array

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
img_gray = img.convert('L')

# create a new figure
figure();   

#show hist
"""
#hist() takes a one-dimensional array as input
#flatten() converts any array to a one-dimensional array with values taken row-wise
"""
hist(array(img_gray).flatten(),10)   

show()

