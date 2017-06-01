# -*- coding: utf-8 -*-
#from opencv.highgui import *
import sys
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import cv2
import os

def load_all_images(dir):
    imgs = []
    for file_name in os.listdir(dir):
        if os.path.splitext(file_name)[-1] == '.png':
            # Remember that I had to flip the iPhone image, also the image was in BGR colorspace so I had to convert to RGB
            img = cv2.cvtColor(cv2.imread(os.path.join(dir, file_name)), cv2.COLOR_BGR2RGB)[::-1, ::-1, :]
            imgs.append(img)

    return imgs

def build_gif(imgs, show_gif=True, save_gif=True, title=''):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_axis_off()

    ims = map(lambda x: (ax.imshow(x), ax.set_title(title)), imgs)
    # call the animator. blit=True means only re-draw the parts that # have changed.
    im_ani = animation.ArtistAnimation(fig, ims, interval=100, repeat_delay=0, blit=True)

    if save_gif:
        im_ani.save('animation.gif', writer='imagemagick')

    if show_gif:
        plt.show()

    return

if __name__ == "__main__":
    imgs = load_all_images(sys.argv[1])
    build_gif(imgs)
