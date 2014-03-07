"""
    open an image file and show it.
"""

from PIL import Image
from pylab import imshow,show,subplot,array,figure

file_name='../../data/cv_data/empire.jpg'
figure()
# load the image file
img = Image.open(file_name)

# convert to gray
img_gray = img.convert('L')    # not inplace operator

# show the two pics  on 1*2 frame
subplot(1,2,1)   
imshow(img)
subplot(1,2,2)
imshow(img_gray)

# starts the figure GUI and raises the figure windows
show()
