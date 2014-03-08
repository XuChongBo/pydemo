from PIL import Image
from pylab import imshow,show,subplot,array,figure,axis

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')

#crop and rotate
box = (200,200,300,300)     #(left, upper, right, lower)
region = img.crop(box)      #just copy out

#do roate
print 'before rotate:', region
region = region.rotate(45)
print 'after rotate:', region

#do resize
img=img.resize((200,200))

# plot the image
figure()
subplot(1,2,1)   
imshow(region)
subplot(1,2,2)
imshow(img)

show()
