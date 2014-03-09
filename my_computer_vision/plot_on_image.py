from PIL import Image
from pylab import imshow,show,plot,array,figure,axis,title

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')

imshow(img)

# some points.  one column stands for one point (x,y)
x = [100,100,400,400,450]
y = [200,500,200,500,420]

# -----plot line connecting the points
plot(x,y)# default blue solid line
#plot(x,y,'go-') # green line with circle-markers
#plot(x,y,'ks:') # black dotted line with square-markers
plot(x[:2],y[:2]) # plot line connecting the first two points

# -----plot the points with red star-markers
plot(x,y,'r*')


# add title and show the plot
title('Plotting: "empire.jpg"')
show()
