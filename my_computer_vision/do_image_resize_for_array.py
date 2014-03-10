from PIL import Image
from pylab import imshow,show,subplot,array,figure,axis,uint8,gray

def img_array_resize(img,sz):
    """ Resize an image array using PIL. 
        input: img can be array(must has two dimensions) or pil image.
        output: resized array
    """ 
    t = Image.fromarray(uint8(img))
    return array(t.resize(sz))

a=array([[45,45,89],[4,3,2],[5,6,7]])
print "origional:"
print a,type(a),a.shape, a.dtype


#---- normal resize funtion of numpy array
b=a.copy()
b.resize((10,10))  # it is a in-place operation
print "array resize:"
print b,type(b),b.shape, b.dtype

#--- image resize that will perform the interxx


c=img_array_resize(a,(10,10))
print "image resize:"
print c,type(c),c.shape, c.dtype

