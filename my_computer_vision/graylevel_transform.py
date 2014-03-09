from PIL import Image
from pylab import imshow,show,axis,array,figure
from pylab import gray,subplot

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
img=array(img) 
#img=array(img.convert('L')) 

figure()
gray() # don't use colors 
subplot(1,4,1)   
imshow(img)

subplot(1,4,2)   
#NumPy will always change the array type to the "lowest" type that can represent the data
im2 = 600 - img  # the return type will always  fit the result  
imshow(im2)

subplot(1,4,3)   
#im3 = (100.0/255) * img + 100   #clamp to interval 100...200 
im3 = 255 - img   #invert image
imshow(im3)

subplot(1,4,4)   
im4 = 255.0 * (img/255.0)**2     #squared
imshow(im4)

print img.shape, img.dtype
print img.min(), img.max()
print im2.shape, im2.dtype
print im2.min(), im2.max()
print im3.shape, im3.dtype
print im3.min(), im3.max()
print im4.shape, im4.dtype
print im4.min(), im4.max()

show()
