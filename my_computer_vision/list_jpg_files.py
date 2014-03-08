import os
from PIL import Image 

def get_jpg_list(path):
    """ Returns a list of filenames for all jpg images in a directory. """
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.jpg')]

def print_files(file_list):
    for item in file_list: 
        print item
        print os.path.splitext(item)[0]

if __name__=="__main__":
    l=get_jpg_list('../../data/cv_data/')
    print_files(l)
