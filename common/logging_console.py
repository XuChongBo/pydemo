#!/usr/bin/env python
# -*- coding:utf-8 -*-

#borrow from DIGITS

import sys
import os.path
import time
import argparse
import logging
import operator
from PIL import Image


# logging.basicConfig(
#     level=logging.DEBUG,
#     format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
# )
# 使用一个名字为abc的logger
logger = logging.getLogger('log')
# 设置logger的level为DEBUG
logger.setLevel(logging.DEBUG)
# 创建一个输出日志到控制台的StreamHandler
hdr = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)
# 给logger添加上handler
logger.addHandler(hdr)



def print_datum(datum):
    """
    Utility for printing a datum
    """
    logger.debug('\tWxHxC:   %sx%sx%s' % (datum.width, datum.height, datum.channels))
    logger.debug('\tLabel:   %s' % (datum.label if datum.HasField('label') else 'None',))
    logger.debug('\tEncoded: %s' % datum.encoded)


