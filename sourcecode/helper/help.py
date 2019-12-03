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
import statistics


def analizeResult(result):
    res = {}
    res["  max"] = max(result)
    res["  min"] = min(result)
    res["  mid"] = statistics.median(result)
    res["  avg"] = statistics.mean(result)
    res["  var"] = statistics.variance(result)
    res["stdev"] = statistics.stdev(result)
    return res


def isFileExist(filename):
    return path.exists(filename)


def today():
    return datetime.datetime.now()


def getLevelFileName(level, id):
    return './dataset/cambridge/'+level+'/'+str(id)+'.txt'
