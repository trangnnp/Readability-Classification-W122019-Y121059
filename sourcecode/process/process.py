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


def tokenize(document):
    document = document.replace('-', '')
    document = document.replace('\n', ' ')
    tokenizer = RegexpTokenizer(r'[A-Za-z0-9]+')
    # TODO: remove white spaces
    # TODO: tokenize
    document = tokenizer.tokenize(document)
    return document


def preprocess(document):
    processed_word = []
    # TODO: lowercase
    document = document.lower()
    # TODO: remove number
    document = ''.join([i for i in document if (not i.isdigit())])
    # TODO: remove punctuation
    document = document.replace('-', '')
    tokenizer = RegexpTokenizer(r'[A-Za-z]+')
    # TODO: remove white spaces
    # TODO: tokenize
    processed_word = tokenizer.tokenize(document)
    # TODO: remove stopword
    processed_word = [
        word for word in processed_word if word not in stopwords.words('english')]
    # stemming/lemmatization
    lemmatizer = WordNetLemmatizer()
    processed_word = [lemmatizer.lemmatize(word) for word in processed_word]
    # processed_word = [stemmer.stem(word) for word in processed_word]
    return processed_word


def readLevel(docName, quantyLevel):
    l.startHere('Start Reading ' + docName)

    levelData = []
    preprocessedLevelData = []
    scoreDoc = []
    for i in range(1, quantyLevel+1):
        fileName = h.getLevelFileName(docName, i)
        fi = open(fileName, 'r')
        levelData.append(fi.read())
        # l.startHere("Preprocess " + fileName + " Start")
        preprocessedLevelData.append(preprocess(levelData[-1]))
        levelData[-1] = tokenize(levelData[-1])
        scoreDoc.append(calculateScore(
            levelData[-1], preprocessedLevelData[-1]))
        l.doneHere("Preprocess " + fileName + " Done")
    l.doneHere('Read ' + docName + ' Done')
    return levelData, preprocessedLevelData, scoreDoc


def readTest(level, test):
    # print(level)
    fileName = h.getLevelFileName(level, test)
    l.startHere('Reading Test ' + fileName + ' Start')

    fi = open(fileName, 'r')
    raw = fi.read()
    l.startHere("Preprocess " + fileName + " Start")
    preprocessed = preprocess(raw)
    raw = tokenize(raw)
    l.doneHere("Preprocess " + fileName + " Done")
    l.doneHere('Reading Test ' + fileName + ' Done')
    # print(raw)
    # print(preprocessed)
    return raw, preprocessed


def getLimitLevel(level, score, testList):
    l.startHere("Limiting " + level + " Start")
    limit = []
    for i in range(len(score)):
        if (i+1 not in testList):
            limit.append(score[i])
            l.resultHere('Score on ' + level + ' Limiting: ' + str(limit[-1]))
    analys = h.analizeResult(limit)
    for key in analys:
        l.resultHere(key + ': ' + str(analys[key]))
    l.doneHere("Limiting " + level + " Done")
    return float((analys["  mid"]+analys["  max"]))/2


def avgSyllableCount(words):
    syllable = []
    for w in words:
        syllable.append(h.syllableCount(w))
    return float(sum(syllable))/float(len(syllable))


def getScore(level, raw, preprocessed):
    # l.startHere("Scoring " + level + " Start")
    score = calculateScore(raw, preprocessed)
    l.resultHere('Score on ' + level + ' Limiting: ' + str(score))
    # l.doneHere("Scoring " + level + " Done")
    return score


def finalScore(score):
    final = 0.0
    for key in score:
        final += score[key]
    return final


def calculateScore(raw, preprocessed):
    score = {
        "lexical_density": 0.0,
        "char_per_word": 0.0,
        "type_token_ratio": 0.0,
        "syllable_count": 0.0
    }

    voca = set(preprocessed)
    vocaRaw = set(raw)
    type_token_ratio = "type_token_ratio"
    lexical_density = "lexical_density"
    char_per_word = "char_per_word"
    syllable_count = "syllable_count"

    # Token related
    # ___type_token_ratio
    score[type_token_ratio] = float(len(voca))/float(len(raw))
    # l.resultHere('type_token_ratio: ' + str(score[type_token_ratio]))

    # Lexical related
    # ___lexical_density
    s = set()
    s.update(preprocessed)
    score[lexical_density] = float(len(s)/len(raw))
    # l.resultHere('lexical_density: ' + str(score[lexical_density]))

    # Character related
    # ___char_per_word
    for char in voca:
        score[char_per_word] += len(char)
    score[char_per_word] = float(score[char_per_word]/len(voca))
    # l.resultHere('char_per_word: ' + str(score[char_per_word]))

    # ___syllable_count
    score[syllable_count] = avgSyllableCount(preprocessed)

    return finalScore(score)


def evaluate(level, testList, result):
    score = 0.0
    for i in range(len(result)):
        levelAcc = float(result[i])/float(len(testList[i]))
        score += levelAcc
        l.resultHere('Accurrancy on '+level[i]+': '+str(levelAcc))
        print('Accurrancy on '+level[i]+': '+str(levelAcc))
    return float(score)/float(len(result))


def main():
    l.callHere('Start main processing!')
    print("Start processing...")
    print("Start training...")

    l.startHere('Start Prepare Traning data')

    level = ['KET', 'PET', 'FCE', 'CAE', 'CPE']
    quantyLevel = [50, 50, 50, 50, 50]
    # quantyLevel = [5, 5, 5, 5, 5]

    l.startHere('Initialize parameters Start')
    levelLimit = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    l.doneHere('Initialize parameters Done')

    testList = setupFold(quantyLevel)
    accurancy = []
    levelDocs = {}
    preprocessLevelDocs = {}
    scoreDoc = {}
    for i in range(len(level)):
        levelDocs[i], preprocessLevelDocs[i], scoreDoc[i] = readLevel(
            level[i], quantyLevel[i])

    for timee in range(int(cc.FOLD)):
        print('\nTime ' + str(timee) + ' Start')
        l.startHere('Time ' + str(timee) + ' Start')
        l.startHere('Start Training data')

        for i in range(len(level)):
            levelLimit[i] = getLimitLevel(
                level[i], scoreDoc[i], testList[timee][i])

        for i in range(len(level)):
            l.resultHere('Level Limit on ' + level[i]+': '+str(levelLimit[i]))
        l.doneHere('Traning data Done')

        print("Start testing...")
        l.startHere('Test Start')
        testResult = [0, 0, 0, 0, 0]

        for i in range(len(level)):
            for test in testList[timee][i]:
                score = scoreDoc[i][test-1]
                if score <= levelLimit[i] and score > levelLimit[i-1]:
                    testResult[i] += 1
        l.doneHere('Test Done')

        print("Start evaluate...")
        l.startHere('Evaluate Start')

        l.doneHere('Evaluate Done')
        accurancy.append(evaluate(level, testList[timee], testResult))
        l.resultHere('Accurrancy:        ' + str(accurancy[-1]))
        print('Accurrancy:        ' + str(accurancy[-1]))
        l.doneHere('Time ' + str(timee) + ' Done')

    finalAccurrancy = float(sum(accurancy))/float(len(accurancy))
    l.resultHere('Final Accurrancy:  ' + str(finalAccurrancy))
    print('Final Accurrancy:  ' + str(finalAccurrancy))

    l.exitHere('Exit main process!')


if __name__ == "__main__":
    main()
