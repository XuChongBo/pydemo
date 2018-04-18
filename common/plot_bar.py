#!/usr/bin/env python
# -*- coding:utf-8 -*-
#coding=utf-8
""" Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt
#plt.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体,解决中文显示问题
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
n_groups = 6

means_men = (0.20, 0.35, 0.30, 0.35, 0.27, 0.18)
#std_men = (2, 3, 4, 1, 2)
means_women = (0.20, 0.35, 0.30, 0.35, 0.27, 0.18)

#std_women = (3, 5, 2, 3, 3)

fig, ax = plt.subplots()

index = np.arange(n_groups)
#bar_width = 0.35
bar_width = 0.2
opacity = 0.4
error_config = {'ecolor': '0.3'}

rects1 = plt.bar(index, means_men, bar_width,
                 alpha=opacity,
                 color='b',
                 #yerr=std_men,
                 error_kw=error_config,
                 label='Men')

rects2 = plt.bar(index + bar_width, means_women, bar_width,
                 alpha=opacity,
                 color='r',
                 #yerr=std_women,
                 error_kw=error_config,
                 label='Women')
def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2.0, 1.05*height, 
                '%.2f' % height, ha='center', va='bottom')
autolabel(rects1)
autolabel(rects2)


plt.xlabel(u'n')
plt.ylabel(u'people')
plt.title(u'stats')
plt.xticks(index + bar_width, ('1', '2', '3', '4', '5', '6'))
#plt.legend()
ax.set_ybound(0, 1)

plt.tight_layout()
plt.show()
#plt.savefig(u't.png')
