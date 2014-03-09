from PIL import Image
from pylab import imshow,show,axis,array

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')

img=array(img) 

#invert image
im2 = 255 - img                 

imshow(im2)

show()
