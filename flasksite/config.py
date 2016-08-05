#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

#APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# redis 
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

# paths
LABELED_DATASET_PATH = '/data/stroke_images'
UNLABELED_DATASET_PATH = '/data/unlabeled_stroke_images'

##
LOG_FILE_PATH = '/logs/handwriting.log'
IMAGE_WIDTH = 109
