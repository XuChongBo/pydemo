import os
from PIL import Image 
from pylab import imshow,show,axis,array,zeros

def get_jpg_list(path):
    """ Returns a list of filenames for all jpg images in a directory. """
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

def browse_image_files(file_list):
    for item in file_list: 
        print item
        img = Image.open(item)
        imshow(img)
        show()

if __name__=="__main__":
    l=get_jpg_list('../../data/cv_data/')
    browse_image_files(l)
