
from PIL import Image
from pylab import imshow,show,axis,array,figure
from pylab import gray,subplot,uint8

img = Image.new( 'RGB', (200,200) )

imshow(img)
img.save("blank.png", "png")
show()

