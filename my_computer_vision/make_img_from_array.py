
from PIL import Image
from pylab import imshow,show,axis,array,figure
from pylab import gray,subplot,uint8
# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
img=array(img) 
print img.min(), img.max()

img=img*1000
print img.min(), img.max()
print img.shape, img.dtype

img=uint8(img)
print img.min(), img.max()
print img.shape, img.dtype
img_new = Image.fromarray(img)   #the input array must be type of 'uinit8' 

imshow(img_new)
show()

