from PIL import Image

from pylab import imshow,axis,contour,axis, figure,gray,hist,show
from numpy import array
from pylab import subplot,plot

# load the image file
img = Image.open('../../data/cv_data/empire.jpg')
img_gray = img.convert('L')

def get_statistic(img_gray):
    """
    assume the shape of img array is (height, width).
    """
    t = array(img_gray)
    h = array([0]*256)
    print t.shape
    assert(t.ndim==2)
    for i in range(t.shape[0]):
        for j in range(t.shape[1]):
            h[t[i,j]]+=1
    #print h
    return h

#-------  Method 1 ---------------------------------
h = get_statistic(img_gray)    
# create a new figure
figure();   
subplot(1,2,1)
plot(range(len(h)),h)


#-------  Method2 ---------------------------------
"""
#hist() takes a one-dimensional array as input
#flatten() converts any array to a one-dimensional array with values taken row-wise
"""
subplot(1,2,2)
hist(array(img_gray).flatten(),10)   

show()


