import cv2

img1 = cv2.imread('/Users/xcbfreedom/projects/data/lena.jpg')

img2 = img1.copy()
img3 = img1.copy()

fps=15
height , width , layers =  img1.shape
filename='/Users/xcbfreedom/Documents/video.avi'
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case

if 1:
    video = cv2.VideoWriter(filename,fourcc,fps,(width,height))
else:    
    video= cv2.VideoWriter()
    success = video.open(filename,fourcc,fps,(width,height),True) 

video.write(img1)
video.write(img2)
video.write(img3)
video.release()
