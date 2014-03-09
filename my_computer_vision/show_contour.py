from PIL import Image
from pylab import imshow,show,axis,contour,axis, figure,gray,hist
from pylab import array

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
img_gray = img.convert('L')

# create a new figure
figure(); gray(); axis('equal'); axis('off')

# show contours with origin upper left corner
contour(img_gray, origin='image')

show()
