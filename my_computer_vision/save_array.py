from PIL import Image
from pylab import imshow,show,axis,array,zeros,uint8,imsave
from pylab import jet

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')

img=array(img) 

#invert image
im2 = 255 - img                 

im3 = zeros(im2.shape)
im3[15:15+10,15:15+10]=200
#
im4 = uint8(im3)
#Image.fromarray(im4).save('test.png')  # im4 must be uinit8 type

#http://docs.scipy.org/doc/scipy/reference/misc.html#scipy.misc.comb
imsave('test.png', im4)

print im4[15:15+10,15:15+10]

imshow(im4)
show()
