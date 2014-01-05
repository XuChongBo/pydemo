import cv2
import os
import time
#height , width , layers =  img1.shape

dir_path='/Users/xcbfreedom/projects/data/dogs_vs_cats'
#fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case

#videoCapture = cv2.VideoCapture(filename)
#fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
#size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))

cv2.namedWindow("Example1")
num=0

dir_list = os.walk(dir_path)
for root, dirs, files in dir_list:
    for f in files:
        num+=1
        filename=os.path.join(root, f)
        print num
        img=cv2.imread(filename)
        img=cv2.resize(img, (100,100))
        cv2.imshow( "Example1", img)
        if 27==cv2.waitKey(1000):
            break
