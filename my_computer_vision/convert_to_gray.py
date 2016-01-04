from PIL import Image
from pylab import imshow,show,subplot,array,figure,gray

file_name='../../data/cv_data/empire.jpg'
# load the image file
img = Image.open(file_name)
print img

# convert to gray
img_gray = img.convert('L')    # not inplace operator
print img_gray


figure()
gray() # don't use colors 

# show the two pics  on 1*2 frame
subplot(1,2,1)   
imshow(img)
subplot(1,2,2)
imshow(img_gray)

# starts the figure GUI and raises the figure windows
show()


##
# for opencv image
# b = im[:,:,0]
# g = im[:,:,1]
# r = im[:,:,2]
#im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
#im_gray = ( r*0.3 + 0.59*g + 0.11*b ).astype(np.uint8)
