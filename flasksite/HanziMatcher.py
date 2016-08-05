#!/usr/bin/env python
# -*- coding:utf-8 -*-


from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import codecs
import config
import utils
from hanzi import Hanzi
import os
from flask import current_app
from Stroke import Location, Direction
hanziDictonary = {}    #tag->list

def load_data_of_the_tag(tag):
    # if tag in hanziDictonary:
    #     return
    hanziDictonary[tag] = []
    #print tag, type(tag)
    filepathList = current_app.redis.lrange(tag.encode("utf-8")+"_pathlist", 0, -1)
    print "in browse total", len(filepathList)
    print filepathList

    for filepath in filepathList:
        current_app.logger.info(filepath.decode('utf-8'))
        png_filepath = filepath.strip()
        svg_filepath = png_filepath[:-3]+"svg"
        print svg_filepath, type(svg_filepath)
        thelist = hanziDictonary.setdefault(tag,[])
        thelist.append( Hanzi.parse_from_file(svg_filepath) )

def check_the_tag(hanzi):
    load_data_of_the_tag(hanzi.tag)
    # check if some exmaple in the sample set match the hanzi 
    maxScore = 0
    for item in hanziDictonary[hanzi.tag]:
        score = match_score(hanzi.features, item.features)
        current_app.logger.debug("match_score:%s", score)
        if score>=80:
            return True,score
        if score>maxScore:
            maxScore = score
    return False, maxScore
    # check if hit the max similarity


def match_score(theOne, other):
    # return fuzzyComparer.getMatchScore(other);
    # the weight for each feature
    STROKE_DIRECTION_WEIGHT = 1.0
    MOVE_DIRECTION_WEIGHT = 0.8
    STROKE_LOCATION_WEIGHT = 0.6   
    # soft match weight decay
    CLOSE_WEIGHT = 0.7                  
    score = 0.0
    if theOne['strokeNum']!=other['strokeNum']:
        current_app.logger.debug("strokeNum NOT match")
        return 0.0
    for i in range(theOne['strokeNum']):
        current_app.logger.debug("===check stroke:%s====", i)
        #// Stroke direction
        if theOne['strokeDirections'][i] == other['strokeDirections'][i]:
            score += STROKE_DIRECTION_WEIGHT
            current_app.logger.debug("STROKE_DIRECTION match: +%s", STROKE_DIRECTION_WEIGHT)
        elif Direction.isClose(theOne['strokeDirections'][i], other['strokeDirections'][i]):
            score += STROKE_DIRECTION_WEIGHT * CLOSE_WEIGHT;
            current_app.logger.debug("STROKE_DIRECTION close: +%s", STROKE_DIRECTION_WEIGHT * CLOSE_WEIGHT)
        #// Move direction
        if i>0:
            if theOne['moveDirections'][i-1] == other['moveDirections'][i-1]:
                score += MOVE_DIRECTION_WEIGHT
                current_app.logger.debug("MOVE_DIRECTION match: +%s", MOVE_DIRECTION_WEIGHT)
            elif Direction.isClose(theOne['moveDirections'][i-1], other['moveDirections'][i-1]):
                score += MOVE_DIRECTION_WEIGHT * CLOSE_WEIGHT
                current_app.logger.debug("MOVE_DIRECTION close: +%s", MOVE_DIRECTION_WEIGHT * CLOSE_WEIGHT)
        
        #// Start and end locations
        if theOne['strokeStarts'][i] == other['strokeStarts'][i]:
            score += STROKE_LOCATION_WEIGHT
            current_app.logger.debug("STROKE_LOCATION_START match: +%s", STROKE_LOCATION_WEIGHT)
        elif Location.isClose(theOne['strokeStarts'][i], other['strokeStarts'][i]):
            score += STROKE_LOCATION_WEIGHT * CLOSE_WEIGHT;
            current_app.logger.debug("STROKE_LOCATION_START close: +%s", STROKE_LOCATION_WEIGHT * CLOSE_WEIGHT)

        if theOne['strokeEnds'][i] == other['strokeEnds'][i]:
            score += STROKE_LOCATION_WEIGHT
            current_app.logger.debug("STROKE_LOCATION_END match: +%s", STROKE_LOCATION_WEIGHT)
        elif Location.isClose(theOne['strokeEnds'][i], other['strokeEnds'][i]):
            score += STROKE_LOCATION_WEIGHT * CLOSE_WEIGHT;
            current_app.logger.debug("STROKE_LOCATION_END close: +%s", STROKE_LOCATION_WEIGHT * CLOSE_WEIGHT)

    maxv = len(theOne['strokeStarts'])*(STROKE_DIRECTION_WEIGHT+2*STROKE_LOCATION_WEIGHT)+(len(theOne['strokeStarts'])-1) * MOVE_DIRECTION_WEIGHT
    ret_score = int(100.0*score / maxv)
    current_app.logger.debug("score=%s", score)
    current_app.logger.debug("ret_score = 100*%s/%s = %s", score,maxv,ret_score)
    return ret_score

