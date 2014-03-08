from PIL import Image 

img = Image.open('../../data/cv_data/empire.jpg')
img.save('./test.png')
