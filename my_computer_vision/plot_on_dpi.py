import matplotlib.pyplot as plt
import numpy as np

# DPI, here, has _nothing_ to do with your screen's DPI.
dpi = 10.0
xpixels, ypixels = 200, 200

fig = plt.figure(figsize=(ypixels/dpi, xpixels/dpi), dpi=dpi)
fig.figimage(np.random.random((xpixels, ypixels)))
plt.show()
