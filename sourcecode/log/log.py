from config import config as c
from helper import help as h


def wLog(tag, context):
    f = open(c.logFile(), 'a')
    context = str(h.today()) + ':   ['+tag+']   '+context + '\n'
    f.write(context)
    f.close()


def callHere(context):
    wLog('INFO', context)


def exitHere(context):
    wLog('EXIT', context)
