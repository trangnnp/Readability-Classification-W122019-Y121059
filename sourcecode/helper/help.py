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
import re
import random
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import stopwords
from nltk import word_tokenize
from collections import Counter
import operator
from random import randrange
from helper import help as h
from config import constant as cc
from config import config as c
import numpy
import string
import re
import os
import sys
sys.setrecursionlimit(1000000)


def syllableCount(word):
    word = word.lower()

    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables

    exception_add = ['serious', 'crucial']
    exception_del = ['fortunately', 'unfortunately']

    co_one = ['cool', 'coach', 'coat', 'coal', 'count', 'coin', 'coarse',
              'coup', 'coif', 'cook', 'coign', 'coiffe', 'coof', 'court']
    co_two = ['coapt', 'coed', 'coinci']

    pre_one = ['preach']

    syls = 0  # added syllable number
    disc = 0  # discarded syllable number

    # 1) if letters < 3 : return 1
    if len(word) <= 3:
        syls = 1
        return syls

    # 2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.
    # if it has only 1 vowel or 1 set of consecutive vowels, discard. (like "speed", "fled" etc.)

    if word[-2:] == "es" or word[-2:] == "ed":
        doubleAndtripple_1 = len(re.findall(r'[eaoui][eaoui]', word))
        if doubleAndtripple_1 > 1 or len(re.findall(r'[eaoui][^eaoui]', word)) > 1:
            if word[-3:] == "ted" or word[-3:] == "tes" or word[-3:] == "ses" or word[-3:] == "ied" or word[-3:] == "ies":
                pass
            else:
                disc += 1

    # 3) discard trailing "e", except where ending is "le"

    le_except = ['whole', 'mobile', 'pole', 'male', 'female',
                 'hale', 'pale', 'tale', 'sale', 'aisle', 'whale', 'while']

    if word[-1:] == "e":
        if word[-2:] == "le" and word not in le_except:
            pass

        else:
            disc += 1

    # 4) check if consecutive vowels exists, triplets or pairs, count them as one.

    doubleAndtripple = len(re.findall(r'[eaoui][eaoui]', word))
    tripple = len(re.findall(r'[eaoui][eaoui][eaoui]', word))
    disc += doubleAndtripple + tripple

    # 5) count remaining vowels in word.
    numVowels = len(re.findall(r'[eaoui]', word))

    # 6) add one if starts with "mc"
    if word[:2] == "mc":
        syls += 1

    # 7) add one if ends with "y" but is not surrouned by vowel
    if word[-1:] == "y" and word[-2] not in "aeoui":
        syls += 1

    # 8) add one if "y" is surrounded by non-vowels and is not in the last word.

    for i, j in enumerate(word):
        if j == "y":
            if (i != 0) and (i != len(word)-1):
                if word[i-1] not in "aeoui" and word[i+1] not in "aeoui":
                    syls += 1

    # 9) if starts with "tri-" or "bi-" and is followed by a vowel, add one.

    if word[:3] == "tri" and word[3] in "aeoui":
        syls += 1

    if word[:2] == "bi" and word[2] in "aeoui":
        syls += 1

    # 10) if ends with "-ian", should be counted as two syllables, except for "-tian" and "-cian"

    if word[-3:] == "ian":
        # and (word[-4:] != "cian" or word[-4:] != "tian") :
        if word[-4:] == "cian" or word[-4:] == "tian":
            pass
        else:
            syls += 1

    # 11) if starts with "co-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:2] == "co" and word[2] in 'eaoui':

        if word[:4] in co_two or word[:5] in co_two or word[:6] in co_two:
            syls += 1
        elif word[:4] in co_one or word[:5] in co_one or word[:6] in co_one:
            pass
        else:
            syls += 1

    # 12) if starts with "pre-" and is followed by a vowel, check if exists in the double syllable dictionary, if not, check if in single dictionary and act accordingly.

    if word[:3] == "pre" and word[3] in 'eaoui':
        if word[:6] in pre_one:
            pass
        else:
            syls += 1

    # 13) check for "-n't" and cross match with dictionary to add syllable.

    negative = ["doesn't", "isn't", "shouldn't", "couldn't", "wouldn't"]

    if word[-3:] == "n't":
        if word in negative:
            syls += 1
        else:
            pass

    # 14) Handling the exceptional words.

    if word in exception_del:
        disc += 1

    if word in exception_add:
        syls += 1

    # calculate the output
    return numVowels - disc + syls


# fi = open('coe.txt', 'w')

def setupCoefficient(level, featureCount, unit, topLimit, bottomLimit):
    l.startHere('Start setup Coefficient')
    coe = {}
    fold = int(cc.FOLD)

    curSubSet = []
    for i in range(featureCount):
        curSubSet.append(0.0)

    newCoeSet(-1, featureCount,
              curSubSet, unit, topLimit, bottomLimit)
    print("Coe Done")
    fi.close()

    return coe


def newCoeSet(num, featureCount, curSubSet, unit, topLimit, bottomLimit):
    if sum(curSubSet) > 1:
        return
    num += 1
    if num == featureCount-1:
        curSubSet[-1] = 1-sum(curSubSet[:-1])
        fi.write(str(curSubSet)+'\n')
        curSubSet[-1] = 0.0
        return

    for i in numpy.arange(bottomLimit-unit, topLimit+unit, unit):
        curSubSet[num] = i
        newCoeSet(num, featureCount, curSubSet,
                  unit, topLimit, bottomLimit)
        curSubSet[num] = 0.0

    return


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


def readLevel(docName, quantyLevel, dataset):
    l.startHere('Start Reading ' + docName)

    levelData = []
    preprocessedLevelData = []
    mean_sentence_length = []
    scoreDoc = {
        "lexical_density": [],
        "char_per_word": [],
        "type_token_ratio": [],
        "syllable_count": [],
        "document_length": [],
        "sentence_length": []
    }

    for i in range(1, quantyLevel+1):
        if dataset == 'corpus':
            fileName = h.getLevelFileName1(docName, i)
        else:
            fileName = h.getLevelFileName(docName, i)
        fi = open(fileName, 'r')
        levelData.append(fi.read())
        tmp = re.split(r'[.!?]+', levelData[-1])
        sentence_length = []
        for sen in tmp[:-1]:
            sentence_length.append(len(tokenize(sen)))
        mean_sentence_length.append(statistics.mean(sentence_length))
        preprocessedLevelData.append(preprocess(levelData[-1]))
        levelData[-1] = tokenize(levelData[-1])
        l.doneHere("Preprocess " + fileName + " Done")
    l.doneHere('Read ' + docName + ' Done')
    return levelData, preprocessedLevelData, mean_sentence_length


def calculateRawScore(level, quantyLevel, featureCount, dataset):
    # print("CalculateRawScore start")
    levelDocs = {}
    preprocessLevelDocs = {}
    meanx = {}
    scoreDoc = {}
    for i in range(len(level)):
        levelDocs[i], preprocessLevelDocs[i], meanx[i] = readLevel(
            level[i], quantyLevel[i], dataset)
    # print("Read raw data done...")

    raw = {}
    for i in range(len(level)):
        raw[i] = []
        maxx = []
        for _ in range(featureCount):
            raw[i].append([])
            maxx.append(-1)

        for id in range(quantyLevel[i]):
            rawScoreID = getRawScore(
                levelDocs[i][id], preprocessLevelDocs[i][id])
            for index in range(featureCount-1):
                raw[i][index].append(rawScoreID[index])
        raw[i][-1] = meanx[i]

        for index in range(featureCount):
            maxx[index] = max(max(raw[i][index]), maxx[index])

        # print(raw)
    # print(maxx)

    for i in range(len(level)):
        # fo = open('./dataset/cambridge/'+level[i]+'_raw.txt', 'w')
        fo = open('./dataset/'+dataset+'/'+level[i]+'_raw.txt', 'w')
        for id in range(quantyLevel[i]):
            for index in range(featureCount):
                fo.write(str(raw[i][index][id]) + ' ')
                raw[i][index][id] = float(raw[i][index][id])/float(maxx[index])
            fo.write('\n')

        fo = open('./dataset/'+dataset+'/'+level[i]+'.txt', 'w')
        # fo = open('./dataset/cambridge/'+level[i]+'.txt', 'w')

        for id in range(quantyLevel[i]):
            for index in range(featureCount):
                fo.write(str(raw[i][index][id]) + ' ')
            fo.write('\n')

    # print("Done Calculation")
    # _ = input()


def getRawScoreFromFile(level, quantyLevel):
    raw = {}

    for i in range(len(level)):
        f = open('./dataset/corpus/'+level[i]+'.txt', 'r')
        raw[i] = []
        rl = f.readlines()
        for x in rl:
            x = x[:-2]
            arr = list(map(float, x.split(' ')))
            raw[i].append(arr)
    return raw


def getRealRawScoreFromFile(level, quantyLevel, dataset):
    raw = {}

    for i in range(len(level)):
        f = open('./dataset/'+dataset+'/'+level[i]+'_raw.txt', 'r')
        # f = open('./dataset/corpus/'+level[i]+'_raw.txt', 'r')
        raw[i] = []
        rl = f.readlines()
        for x in rl:
            x = x[:-2]
            arr = list(map(float, x.split(' ')))
            raw[i].append(arr)
    return raw


def getCoedScore(coef, rawScore):
    score = []
    for le in range(len(rawScore)):
        score.append([])
        for i in range(len(rawScore[le])):
            element = []
            for co in range(len(coef)):
                element.append(rawScore[le][i][co]*coef[co])
            element.append(sum(element))
            score[le].append(element)
    return score


def getCoe(fileName):
    f = open(fileName, 'r')
    coe = []
    rl = f.readlines()
    for x in rl:
        x = x[:-2]
        x = x[1:]
        arr = list(map(float, x.split(', ')))
        coe.append(arr)
    return coe
    # print(coe)


def getRawScore(raw, preprocessed):
    score = {
        "lexical_density":      0.0,
        "char_per_word":        0.0,
        "type_token_ratio":     0.0,
        "correct_type_token_ratio":     0.0,
        "syllable_count":       0.0,
        "document_length":      0.0,
        "awl":                  0.0,
        "mean_sentence_length": 0.0
    }

    voca = set(preprocessed)
    vocaRaw = set(raw)
    type_token_ratio = "type_token_ratio"
    correct_type_token_ratio = "correct_type_token_ratio"
    lexical_density = "lexical_density"
    char_per_word = "char_per_word"
    syllable_count = "syllable_count"
    document_length = "document_length"
    awl = "awl"
    mean_sentence_length = "mean_sentence_length"

    # Token related
    # ___type_token_ratio
    score[type_token_ratio] = float(len(voca))/float(len(raw))
    score[correct_type_token_ratio] = float(len(voca))/float((2*len(raw))**0.5)
    # l.resultHere('type_token_ratio: ' + str(score[type_token_ratio]))

    # Lexical related
    # ___lexical_density
    s = set()
    s.update(preprocessed)
    score[lexical_density] = float(len(s)/len(raw))
    # l.resultHere('lexical_density: ' + str(score[lexical_density]))

    score[awl] = len(set(preprocessed) & set(cc.AWL))

    # Character related
    # ___char_per_word
    for char in voca:
        score[char_per_word] += len(char)
    score[char_per_word] = float(score[char_per_word]/len(voca))
    # l.resultHere('char_per_word: ' + str(score[char_per_word]))

    score[document_length] = len(raw)

    # ___syllable_count
    score[syllable_count] = avgSyllableCount(preprocessed)

    # ___syllable_count
    # score[mean_sentence_length] = avgSyllableCount(preprocessed)

    return [score[type_token_ratio],
            score[correct_type_token_ratio],
            score[lexical_density],
            score[char_per_word],
            score[syllable_count],
            score[document_length],
            score[awl]]


def avgSyllableCount(words):
    syllable = []
    for w in words:
        syllable.append(h.syllableCount(w))
    return float(sum(syllable))/float(len(syllable))


def analizeResult(result):
    res = {}
    res["  max"] = max(result)
    res["  min"] = min(result)
    res["  mid"] = statistics.median(result)
    res["  avg"] = statistics.mean(result)
    res["  var"] = statistics.variance(result)
    res["stdev"] = statistics.stdev(result)
    return res


def standardValues(values):
    maxx = max(values)
    for i in range(values):
        values[i] = float(values[i])/float(maxx)


def isFileExist(filename):
    return path.exists(filename)


def today():
    return datetime.datetime.now()


def getLevelFileName(level, id):
    return './dataset/cambridge/'+level+'/'+str(id)+'.txt'


def getLevelFileName1(level, id):
    return './dataset/corpus/'+level+'/'+str(id)+'.txt'


def mix(dataset):
    s = []
    if dataset == 'corpus':
        level = ['Ele', 'Int', 'Adv']
        n = [150, 150, 150]
    else:
        level = ['KET', 'PET', 'FCE', 'CAE', 'CPE']
        n = [50, 50, 50, 50, 44]

        # level = ['KET', 'PET', 'FCE', 'CAE', 'CPE']
    # n = [150, 150, 150]
    # n = [178, 170, 161]

    for i in range(len(n)):
        s.append([])
        while len(s[i]) < n[i]:
            tmp = random.randrange(n[i])+1
            if tmp not in s[i]:
                s[i].append(tmp)

    print(s)

    for i in range(len(n)):
        for ii in range(1, n[i]+1):
            os.rename('./dataset/'+dataset+'/'+level[i]+'/'+str(ii)+'.txt',
                      './dataset/'+dataset+'/'+level[i]+'/a'+str(s[i][ii-1])+'.txt')

    s = []
    for i in range(len(n)):
        s.append([])
        while len(s[i]) < n[i]:
            tmp = random.randrange(n[i])+1
            if tmp not in s[i]:
                s[i].append(tmp)

    for i in range(len(n)):
        for ii in range(1, n[i]+1):
                # print('./dataset/corpus/'+le+'/'+str(i)+'.txt',
                #       './dataset/corpus/'+le+'/'+str(s[i-1])+'.txt')
            os.rename('./dataset/'+dataset+'/'+level[i]+'/a'+str(ii)+'.txt',
                      './dataset/'+dataset+'/'+level[i]+'/'+str(s[i][ii-1])+'.txt')
