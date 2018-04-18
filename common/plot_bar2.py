#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

"""
background:0.897765059069
face_skin:0.834150654327
nose:0.70936657436
lower_lip:0.574037323221
upper_lip:0.55311177752
right_pupilla:0.535489672334
left_pupilla:0.562944017743
right_brow:0.417593302054
left_brow:0.451624901486
right_eye:0.385060044761
left_eye:0.409570536394
teeth:0.213993712094
right_ear:0.223373841122
left_ear:0.179811740034
glasses:0.0
"""


size = 5
x = np.arange(size)
a = np.random.random(size)
b = np.random.random(size)
c = np.random.random(size)

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

plt.bar(x, a, color='g', width=width, label='a')
plt.bar(x + width, b, color='r', width=width, label='b')
plt.bar(x + 2 * width, c, width=width, label='c')
plt.legend()
plt.show()
