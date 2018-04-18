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

#'[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'


if 1:
    logging.basicConfig(
         stream=sys.stdout,
         level=logging.DEBUG,
         format='[%(asctime)s] [%(name)s] [%(levelname)s]:\t%(message)s')
    logger = logging.getLogger('log')

elif 0:
    # 使用一个名字为abc的logger
    logger = logging.getLogger('log')
    # 设置logger的level为DEBUG
    logger.setLevel(logging.DEBUG)
    # 创建一个输出日志到控制台的StreamHandler
    hdr = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s]:\t%(message)s')
    hdr.setFormatter(formatter)
    # 给logger添加上handler
    logger.addHandler(hdr)
else:
    logger = logging.getLogger('log')

logger.info("hel")
logger.debug("hel")
logger.warning("hel")
logger.info("xxxlxlx")

