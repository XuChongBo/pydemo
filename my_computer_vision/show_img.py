"""
    open an image file and show it.
"""
from PIL import Image
from pylab import imshow,show,axis

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')

# plot the image
imshow(img)

# not plot the axises
axis('off')

# starts the figure GUI and raises the figure windows
show()
