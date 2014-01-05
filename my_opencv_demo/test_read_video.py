import cv2
import sys
import time
#height , width , layers =  img1.shape

filename=sys.argv[1]
#filename='/Users/xcbfreedom/Documents/screencast.avi'
#filename='/Users/xcbfreedom/Documents/video.avi'
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case

videoCapture = cv2.VideoCapture(filename)
fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
cv2.namedWindow("Example1")
success, frame = videoCapture.read()
num=0
while success: # Loop until there are no more frames.
    num+=1
    print "got frame:",num,success
    cv2.imshow( "Example1", frame)
    cv2.waitKey(500)
    pos=videoCapture.get(cv2.cv.CV_CAP_PROP_POS_AVI_RATIO)
    print pos
    if pos<=0.0:
        print "reach the end of file"
        cv2.waitKey(0)
        break
    success, frame = videoCapture.read()
