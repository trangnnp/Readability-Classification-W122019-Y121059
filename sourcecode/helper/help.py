import datetime
import os.path
from os import path
from log import log as l


def isFileExist(filename):
    return path.exists(filename)


def today():
    return datetime.datetime.now()
