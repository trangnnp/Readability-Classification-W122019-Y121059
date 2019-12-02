'''
 # @ Author: Trang Ngoc-Phuong Nguyen
 # @ Create Time: 2019-12-02 22:33:02
 # @ Modified by: Trang Ngoc-Phuong Nguyen
 # @ Modified time: 2019-12-02 22:36:48
 # @ Description:
 '''

import datetime
import os.path
from os import path
from log import log as l


def isFileExist(filename):
    return path.exists(filename)


def today():
    return datetime.datetime.now()
