'''
 # @ Author: Trang Ngoc-Phuong Nguyen
 # @ Create Time: 2019-12-02 16:31:56
 # @ Modified by: Trang Ngoc-Phuong Nguyen
 # @ Modified time: 2019-12-02 20:12:02
 # @ Description:
 '''

import sys
import os
import datetime
from config import config as c
from log import log as l
from helper import help as h
from process import process as p


def main():
    l.startProj()
    l.callHere('Hello world!')
    print("Hello world!")

    sys.path.append(os.path.join(sys.path[0], 'config'))
    sys.path.append(os.path.join(sys.path[0], 'helper'))
    sys.path.append(os.path.join(sys.path[0], 'log'))
    sys.path.append(os.path.join(sys.path[0], 'process'))

    l.exitHere('Exit All!')
    print("Done!")

    # h.mix('cambridge')
    # h.mix('corpus')

    p.main()


if __name__ == "__main__":
    main()
