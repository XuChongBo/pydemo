# -*- coding: utf-8 -*-
# First you need to import the libraries in question.
# borrow from blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
import numpy as np
import cv2
import sys
from PIL import Image
from pylab import imshow,show,axis

# For gray image
img = Image.open(sys.argv[1])
imgcv = np.asarray(img.convert('L'))
#imshow(img)
#show()


cv2.imshow('Demo gray Image',imgcv)
cv2.waitKey(0)
cv2.destroyAllWindows()



# For color image
img = Image.open("demo2.jpg")

# The conversion from PIL to OpenCV is done with the handy NumPy method "numpy.array" which converts the PIL image into a NumPy array.
# cv2.cvtColor does the trick for correcting the colour when converting between PIL and OpenCV Image formats via NumPy.
imgcv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#imshow(img)
#show()

# Display the OpenCV image using inbuilt methods.
cv2.imshow('Demo color Image',imgcv)
cv2.waitKey(0)
cv2.destroyAllWindows()