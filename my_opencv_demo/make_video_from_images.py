import cv2
import os
import time
import random


def MakeOfAllImages(video_file_name,images_dir,limit):
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
    fps=2
    height , width =(400,400)
    video = cv2.VideoWriter(video_file_name,fourcc,fps,(width,height))
    num=0
    dir_list = os.walk(images_dir)
    for root, dirs, files in dir_list:
        for f in files:
            filename=os.path.join(root, f)
            img=cv2.imread(filename)
            img=cv2.resize(img, (width,height))
            video.write(img)
            num+=1
            print num
            if num==limit:
                break

    print "total:", num
    video.release()
    
def MakeOfRandomSelectedImages(video_file_name,images_dir,limit):
    fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v') # note the lower case
    fps=2
    height , width =(400,400)
    video = cv2.VideoWriter(video_file_name,fourcc,fps,(width,height))
    dir_list = os.walk(images_dir)
    num=0
    for root, dirs, files in dir_list:
        while True:
            f=files[random.randint(0,len(files)-1)]
            filename=os.path.join(root, f)
            img=cv2.imread(filename)
            img=cv2.resize(img, (width,height))
            video.write(img)
            num+=1
            print num
            if num==limit:
                break
        break
    print "total:", num
    video.release()



if __name__=="__main__":
    images_dir='/Users/xcbfreedom/projects/data/dogs_vs_cats'
    filename='/Users/xcbfreedom/Documents/video.avi'
    #filename='/Users/xcbfreedom/projects/data/dogscats.avi'
    #MakeOfAllImages(filename, images_dir,200)
    MakeOfRandomSelectedImages(filename, images_dir,200)
