#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PIL import ImageDraw,ImageFont
from PIL import Image 
import random
import math, string  
 
 
p="/usr/share/fonts/truetype/freefont/FreeSans.ttf"
class ImageChar():
  def __init__(self, fontColor = (0, 0, 0),
                     size = (100, 40),
                     fontPath = p,
                     bgColor = (255, 255, 255),
                     fontSize = 20):
    self.size = size
    self.fontPath = fontPath
    self.bgColor = bgColor
    self.fontSize = fontSize
    self.fontColor = fontColor
    self.font = ImageFont.truetype(self.fontPath, self.fontSize)
    self.image = Image.new('RGB', size, bgColor)  
 
  def rotate(self):
    self.image.rotate(random.randint(0, 30), expand=0)  
 
 
  def randRGB(self):
    return (random.randint(0, 255),
           random.randint(0, 255),
           random.randint(0, 255))  
 
  def randPoint(self):
    (width, height) = self.size
    return (random.randint(0, width), random.randint(0, height))  
 
  def randLine(self, num):
    draw = ImageDraw.Draw(self.image)
    for i in range(0, num):
      draw.line([self.randPoint(), self.randPoint()], self.randRGB())
    del draw  
 
  def randChinese(self, num):
    gap = 2
    xstart = 0
    import random as pyrandom
    for i in range(0, num):
      txt = pyrandom.choice(['a','b','c'])
      #self.fontSize*0.5 #+ random.randint(0, gap) 
      pos = (xstart,random.randint(0, 3))
      draw = ImageDraw.Draw(self.image)
      draw.text(pos, txt, font=self.font, fill=self.randRGB())
      w,h = draw.textsize(txt, font=self.font)
      print txt,w,h
      del draw  
      xstart += w
      #self.rotate()
    #self.randLine(18)  
 
  def save(self, path):
    self.image.save(path,'jpeg')

if __name__=='__main__':
	ic = ImageChar(fontColor=(100,211, 90))
	ic.randChinese(4)
	ic.save("1.jpeg")
