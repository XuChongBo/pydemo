from skimage import data, io, filter

image = data.coins() # or any NumPy array!
print image.shape,image.dtype

edges = filter.canny(image, sigma=3)
print type(edges)
print edges.shape,edges.dtype

io.imshow(edges)
io.show()
