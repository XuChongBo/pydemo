#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import Image, ImageEnhance
from pylab import imshow,show,axis,array,zeros
import sys

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
    else:
        layer.paste(mark, position)
    # composite the watermark with the layer
    return Image.composite(layer, im, layer)

def paste(im, mask, color, v):
    m = mask.point(lambda i: i == v and 120)
    im.paste(color, m)

def test():
    #im = Image.open('test-face.jpg')
    #mark = Image.open('test.png')
    im = Image.open('/3T/images/girls_face_v0.3/mm/余飘飘/余飘飘3_face_0.jpg') 
    mark = Image.open('/3T/images/girls_mask_v0.3/mm/余飘飘/余飘飘3_mask_0.png')
    print mark
    def cc(v):
        s = 20
        color = 120
        return 120

    #m = mark.point(lambda i: i > 0 and 120)
    #color = (255,0,255)
    #im.paste(color, m)

    #m = mark.point(cc)
    #print m
    s = 20
    paste(im, mark, (255,0,255), 1*s)
    paste(im, mark, (0,0,255), 2*s)
    paste(im, mark, (255,0,0), 3*s)
    paste(im, mark, (0,255,0), 4*s)
    paste(im, mark, (255,255,0), 5*s)
    print "xx"
    imshow(im)
    show()
    sys.exit(0)
    imshow(watermark(im, mark, 'tile', 0.5))
    watermark(im, mark, 'scale', 1.0).show()
    watermark(im, mark, (100, 100), 0.5).show()

    show()

if __name__ == '__main__':
    test()
#该代码片段来自于: http://www.sharejs.com/codes/python/6120
