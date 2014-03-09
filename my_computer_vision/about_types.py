from PIL import Image
from pylab import imshow,show,axis,array

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
print 'loaded from  file: ',img

img_array = array(img) 
print 'convert to array: ', img_array.shape, img_array.dtype

img_float_array = array(img,'f')
print 'convet to float: ', img_float_array.shape, img_float_array.dtype

print '============'
img_gray = img.convert('L')
print 'after convert to gray: ',img_gray

img_gray_array= array(img_gray) 
print 'convert to array: ', img_gray_array.shape, img_gray_array.dtype

img_gray_float_array = array(img_gray,'f')
print 'convet to float: ', img_gray_float_array.shape, img_gray_float_array.dtype

