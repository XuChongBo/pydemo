"""
    open an image file and show it.
"""
import sys
from PIL import Image
from pylab import imshow,show,axis

# load the image file

img = Image.open(sys.argv[1])
#img = Image.open('../../data/cv_data/empire.jpg')
img.show()
# plot the image
imshow(img)

# not plot the axises
axis('off')

# starts the figure GUI and raises the figure windows
show()

print "aaa"

############## method 2 ===========
import matplotlib.pyplot as plt
img = Image.open(sys.argv[1])
plt.imshow(img,cmap=plt.cm.gray)
plt.show()

########## method 3 =====
cv2.imshow("x",np.array(img))
cv2.waitKey(-1)
