'''
 # @ Author: Trang Ngoc-Phuong Nguyen
 # @ Create Time: 2019-12-02 22:36:36
 # @ Modified by: Trang Ngoc-Phuong Nguyen
 # @ Modified time: 2019-12-02 22:37:06
 # @ Description:
 '''


import sys
import os
import datetime
import re
import string
from config import config as c
from config import constant as cc
from log import log as l
from helper import help as h
from random import randrange
import operator
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.tokenize import RegexpTokenizer


def setupFold(quantyLevel):
    l.startHere('Start setup FOLD')
    foldDict = []
    fold = int(cc.FOLD)

    for i in range(fold):
        foldDict.append({})
        for j in range(len(quantyLevel)):
            foldDict[-1][j] = []
            for id in range(int(quantyLevel[j]/fold)*i+1, int(quantyLevel[j]/fold)*(i+1)+1):
                foldDict[-1][j].append(id)
    l.startHere('Setup FOLD Done')
    return foldDict


def getLimitLevel(level, score, testList):
    l.startHere("Limiting " + level + " Start")
    limit = []
    for i in range(len(score)):
        if (i+1 not in testList):
            limit.append(score[i])
            # l.resultHere('Score on ' + level + ' Limiting: ' + str(limit[-1]))
    analys = h.analizeResult(limit)
    for key in analys:
        l.resultHere(key + ': ' + str(analys[key]))
    l.doneHere("Limiting " + level + " Done")
    return float((analys["  mid"]+analys["  max"]))/2


def evaluate(level, testList, result, size):
    score = 0.0
    acc = []
    for i in range(size):
        levelAcc = float(result[i])/float(len(testList[i]))
        score += levelAcc
        acc.append(levelAcc)
        l.resultHere('Accurrancy on '+level[i]+': '+str(levelAcc))
        # print('Accurrancy on '+level[i]+': '+str(levelAcc))
    return float(score)/float(size), acc


def main():
    l.callHere('Start main processing!')
    print("Start processing...")
    print("Start training...")

    l.startHere('Start Prepare Traning data')

    level = ['KET', 'PET', 'FCE', 'CAE', 'CPE']
    # quantyLevel = [50, 50, 50, 50, 44]

    # quantyLevel = [61, 55, 67, 55, 44]
    # h.calculateRawScore(level, quantyLevel, cc.FEATURE, 'cambridge')
    # _ = input()
    # quantyLevel = [151, 151, 151]
    quantyLevel = [50, 50, 50, 50, 44]

    rawScore = h.getRealRawScoreFromFile(level, quantyLevel, 'cambridge')
    # for i in range(len(rawScore)):
    #     summ = 0
    #     for ii in range(len(rawScore[i])):
    #         summ += rawScore[i][ii][2]
    #     print(summ/len(rawScore[i]))
    # _ = input()

    for i in range(len(rawScore)):
        for ii in range(len(rawScore[i])):
            rawScore[i][ii][-2] = rawScore[i][ii][-2]**0.7

    coe = [[2.256, 0.7, 0.0, 0.0, 0.855, 1.0, 2.0, 0.004, 0.002, 0.085]]
    # coe = [[2.256, 0.7, 0.855, 1.0, 2.0, 0.004, 0.002, 0.085]]
    # coe = [[2.0, 0.7, 1.0, 1.0, 2.0, 0.004, 0.0, 0.085]] 0.8171296296296297

    l.startHere('Initialize parameters Start')
    levelLimit = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    l.doneHere('Initialize parameters Done')

    testList = setupFold(quantyLevel)
    accurancy = []
    levelDocs = {}
    preprocessLevelDocs = {}
    scoreDoc = {}

    for i in range(len(level)):
        scoreDoc[i] = []
        score = 0.0
        for ii in range(len(rawScore[i])):
            score = 0.0
            for iii in range(cc.FEATURE):
                score += rawScore[i][ii][iii]*coe[0][iii]
            scoreDoc[i].append(score)

    acclevel = [[], [], [], [], []]
    for timee in range(int(cc.FOLD)):
        # print('\nTime ' + str(timee) + ' Start')
        l.startHere('Time ' + str(timee) + ' Start')
        l.startHere('Start Training data')

        for i in range(len(level)):
            levelLimit[i] = getLimitLevel(
                level[i], scoreDoc[i], testList[timee][i])

        for i in range(len(level)):
            l.resultHere('Level Limit on ' + level[i]+': '+str(levelLimit[i]))
        l.doneHere('Traning data Done')

        # print("Start testing...")
        l.startHere('Test Start')
        testResult = [0, 0, 0, 0, 0]

        coee = 1.0

        for i in range(len(level)):
            for test in testList[timee][i]:
                score = scoreDoc[i][test-1]
                if score <= levelLimit[i]*coee and score > levelLimit[i-1]*coee:
                    testResult[i] += 1
        l.doneHere('Test Done')

        # print("Start evaluate...")
        l.startHere('Evaluate Start')

        l.doneHere('Evaluate Done')
        a, b = evaluate(level, testList[timee], testResult, 5)
        for i1 in range(len(level)):
            acclevel[i1].append(b[i1])
        accurancy.append(a)
        # accurancy.append(evaluate(level, testList[timee], testResult, 5))
        l.resultHere('Accurrancy:        ' + str(accurancy[-1]))
        # print('Accurrancy:        ' + str(accurancy[-1]))
        l.doneHere('Time ' + str(timee) + ' Done')

    for i in range(len(level)):
        print(level[i], float(sum(acclevel[i]))/cc.FOLD)
    finalAccurrancy = float(sum(accurancy))/float(len(accurancy))
    l.resultHere('Final Accurrancy:  ' + str(finalAccurrancy))
    print('Final Accurrancy Cambridge:  ' + str(finalAccurrancy))

    l.exitHere('Exit main process!')

    level = ['Ele', 'Int', 'Adv']
    # quantyLevel = [178, 170, 161]
    quantyLevel = [150, 150, 150]
    # h.calculateRawScore(level, quantyLevel, cc.FEATURE, 'corpus')
    rawScore = h.getRealRawScoreFromFile(level, quantyLevel, 'corpus')

    # for i in range(len(rawScore)):
    #     summ = 0
    #     for ii in range(len(rawScore[i])):
    #         summ += rawScore[i][ii][2]
    #     print(summ/len(rawScore[i]))
    # _ = input()

    for i in range(len(rawScore)):
        for ii in range(len(rawScore[i])):
            rawScore[i][ii][-2] = rawScore[i][ii][-2]**0.3
    levelLimit = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    testList = setupFold(quantyLevel)
    accurancy = []
    levelDocs = {}
    preprocessLevelDocs = {}
    scoreDoc = {}

    for i in range(len(level)):
        scoreDoc[i] = []
        score = 0.0
        for ii in range(len(rawScore[i])):
            score = 0.0
            for iii in range(cc.FEATURE):
                score += rawScore[i][ii][iii]*coe[0][iii]
            scoreDoc[i].append(score)

    acclevel = [[], [], []]
    for timee in range(int(cc.FOLD)):
        # print('\nTime ' + str(timee) + ' Start')
        l.startHere('Time ' + str(timee) + ' Start')
        l.startHere('Start Training data')

        for i in range(len(level)):
            levelLimit[i] = getLimitLevel(
                level[i], scoreDoc[i], testList[timee][i])

        for i in range(len(level)):
            l.resultHere('Level Limit on ' + level[i]+': '+str(levelLimit[i]))
        l.doneHere('Traning data Done')

        # print("Start testing...")
        l.startHere('Test Start')
        testResult = [0, 0, 0, 0, 0]

        coee = 1.0

        for i in range(len(level)):
            for test in testList[timee][i]:
                score = scoreDoc[i][test-1]
                if score <= levelLimit[i]*coee and score > levelLimit[i-1]*coee:
                    testResult[i] += 1
        l.doneHere('Test Done')

        # print("Start evaluate...")
        l.startHere('Evaluate Start')

        l.doneHere('Evaluate Done')
        a, b = evaluate(level, testList[timee], testResult, 3)
        for i1 in range(len(level)):
            acclevel[i1].append(b[i1])
        accurancy.append(a)
        # accurancy.append(evaluate(level, testList[timee], testResult, 3))
        l.resultHere('Accurrancy:        ' + str(accurancy[-1]))
        # print('Accurrancy:        ' + str(accurancy[-1]))
        l.doneHere('Time ' + str(timee) + ' Done')

    for i in range(len(level)):
        print(level[i], float(sum(acclevel[i]))/cc.FOLD)
    finalAccurrancy = float(sum(accurancy))/float(len(accurancy))
    l.resultHere('Final Accurrancy:  ' + str(finalAccurrancy))
    print('Final Accurrancy Courpus:    ' + str(finalAccurrancy))


if __name__ == "__main__":
    main()
