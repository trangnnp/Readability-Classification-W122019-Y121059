'''
 # @ Author: Trang Ngoc-Phuong Nguyen
 # @ Create Time: 2019-12-02 20:40:14
 # @ Modified by: Trang Ngoc-Phuong Nguyen
 # @ Modified time: 2019-12-02 20:44:34
 # @ Description:
 '''
from helper import help as h


def loadConfig():
    print("Loading Config...")

    print("Config Loaded ><")


def logFile():
    return './sourcecode/log/'+str(h.today())[:10]+'.txt'
