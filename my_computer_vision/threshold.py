from skimage import data, io, filter

image = data.coins() # or any NumPy array!
edges = filter.threshold_adaptive(image,45)
print type(edges)
io.imshow(edges)
io.show()
