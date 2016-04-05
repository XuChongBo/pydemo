#!/usr/bin/env python
# -*- coding:utf-8 -*-

import simplesvg
width = 390 
height = 390
svg = simplesvg.SVG(width, height)
#svg.line(100, 0, 100, 180, stroke = "red", strokeWidth = "1")
svg.polygon([(100, 0), (100, 180)], fill = simplesvg.rgb(0,0,0))

print(svg), type(svg)
print svg.to_xml()

with open("a.svg", "w") as svg_file:
    svg_file.write(svg.to_xml())
