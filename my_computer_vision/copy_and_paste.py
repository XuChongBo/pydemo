from PIL import Image
from pylab import imshow,show,subplot,array,figure,axis

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
img2=img.copy()

#crop
box = (100,100,400,400)  #(left, upper, right, lower)
region = img.crop(box)
print region

#process
#region = region.transpose(Image.ROTATE_180)
#region = region.rotate(180)
region = region.rotate(45)

#paste
img2.paste(region,box)

# plot the image
figure()
subplot(1,2,1)   
imshow(img2)
subplot(1,2,2)
imshow(img)



# not plot the axises
#axis('off')
# starts the figure GUI and raises the figure windows
show()
