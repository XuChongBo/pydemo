from PIL import Image 
import os

in_file = '../../data/cv_data/empire.jpg'
img = Image.open(in_file)

#print os.path.splitext(in_file)[0]+'.png'

img.save('./test.png')
