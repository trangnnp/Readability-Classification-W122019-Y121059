from config import config as c
from helper import help as h


def wLog(tag, context):
    f = open(c.logFile(), 'a')
    context = str(h.today()) + ':   ['+tag+']   '+context + '\n'
    f.write(context)
    f.close()


def startProj():
    wLog('INFO  ', '-----------------------------------------------------------------------------')


def callHere(context):
    wLog('INFO  ', context)


def exitHere(context):
    wLog('EXIT  ', context)


def startHere(context):
    wLog('START ', context)


def doneHere(context):
    wLog('DONE  ', context)


def resultHere(context):
    wLog('RESULT', '----------' + context + '----------')
