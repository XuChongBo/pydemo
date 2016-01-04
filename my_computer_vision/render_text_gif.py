# -*- coding: utf-8 -*-
 
import os
import pygame
 
pygame.init()
#fontfile = '/usr/share/fonts/truetype/myfonts/SIMSUN.TTC' 
fontfile = '/usr/share/fonts/truetype/myfonts/msyh.ttf'
#text = u"本题考查了封建制度"
text = u"第一年出境霉糖"
text = u"点估计第一年"
text = u"内正入第一年"
text = u"湖中中中中"
text = u"分析"
#text = u"出境一年"
font = pygame.font.Font(fontfile, 12)
#font.set_bold(True)
#rtext = font.render(text, False, (0, 0, 0), (255, 255, 255))
rtext = font.render(text, True, (0, 0, 0),(255,255,255))
 
#pygame.image.save(rtext, "t.png")
pygame.image.save(rtext, "t.gif")
