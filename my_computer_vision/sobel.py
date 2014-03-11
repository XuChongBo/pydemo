from skimage import data, io, filter

image = data.coins() # or any NumPy array!

#edges = filter.sobel(image)
edges = filter.canny(image, sigma=3)
print type(edges)
io.imshow(edges)
io.show()
