import random
from importlib import reload
from numpy import *
import random

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],\
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],\
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],\
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'], \
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],\
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec=[0,1,0,1,0,1]      # 1表示侮辱性文字，0表示非侮辱性文字
    return postingList,classVec

def createVocabList(dataSet):
    vocabSet=set([])
    for document in dataSet:
        vocabSet=vocabSet | set(document)
    return list(vocabSet)

def setOfWords2Vec(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]=1
    #    else:print("the word: %s is not in my vocabulary!"%word)
    return returnVec

def bagOfWords2VecMN(vocabList,inputSet):
    returnVec=[0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)]+=1
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numOfDocs=len(trainMatrix)
    numWords=len(trainMatrix[0])
    pAbusive=sum(trainCategory)/float(numOfDocs)
    p0Num=ones(numWords);p1Num=ones(numWords)
    p0Denom=2.0;p1Denom=2.0             #denominator
    for i in range(numOfDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
        else:
            p0Num+=trainMatrix[i]
            p0Denom+=sum(trainMatrix[i])
    p1Vect=log(p1Num/p1Denom)
    p0Vect=log(p0Num/p0Denom)
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify,p0V,p1V,pClass1):
    p1=sum(vec2Classify*p1V)+log(pClass1)
    p0=sum(vec2Classify*p0V)+log(1-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def testingNB():
    listOfPosts,listClasses=loadDataSet()
    myVocabList=createVocabList(listOfPosts)
    trainMat=[]
    for i in listOfPosts:
        trainMat.append(setOfWords2Vec(myVocabList,i))
    p0V,p1V,pAb=trainNB0(trainMat,listClasses)
    testEntry=['love','my','dalmation']
    thisDoc=array(setOfWords2Vec(myVocabList,testEntry))
    # print(thisDoc,'\n',p0V,p1V)
    print(testEntry,'classified as:',classifyNB(thisDoc,p0V,p1V,pAb))
    testEntry = ['stupid', 'garbage']
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
    print(testEntry, 'classified as:', classifyNB(thisDoc, p0V, p1V, pAb))

'''
def textParse(bigString):
    import re
    return [i.lower() for i in re.findall(r'\w*',bigString) if len(i)>2]
'''
def textParse(bigString):
    for k in set([i for i in bigString if i.isalnum()==False and i!='-']):
        bigString=bigString.replace(k,'  ')
    return [i for i in bigString.rstrip('  ').lower().split() if len(i)>2]

def spamText():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):
        wordList=textParse(open('email/spam/%d.txt' % i, encoding='UTF-8',errors='ignore').read())
        docList.append(wordList)
        classList.append(1)
        fullText.extend(wordList)
        wordList = textParse(open('email/ham/%d.txt' % i, encoding='UTF-8',errors='ignore').read())
        docList.append(wordList)
        classList.append(0)
        fullText.extend(wordList)
    vocabList=createVocabList(docList)
    trainingSet=list(range(50));testSet=[]
    for i in range(10):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB0(trainMat,trainClasses)
    errorCount=0.0
    errorList=set()
    for docIndex in testSet:
        wordVector=setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount+=1.0
            errorList|=set(docList[docIndex])
    if(len(errorList)>0):print("classification error", errorList)
    print('the error rate is: %f'%(errorCount/len(testSet)))

def calcMostFreq(vocabList,fullText):
    freqDict={}
    for token in vocabList:
        freqDict[token]=fullText.count(token)
    sortedFreq=sorted(freqDict.items(),key=lambda x:x[1],reverse=True)
    return sortedFreq[:10]

def localWords(feed1,feed0):
    import feedparser
    # feed1=ML=feedparser.parse('https://www.profgalloway.com/feed/')
    # feed0=LW=feedparser.parse('https://www.lesswrong.com/feed.xml?view=curated-rss')
    docList=[];classList=[];fullText=[]
    minLen=min(len(feed1['entries']),len(feed0['entries']))
    for i in range(minLen):
        wordList=textParse(feed1['entries'][i]['title'].split('<')[0])
        docList.append(wordList)
        classList.append(1)
        fullText.extend(wordList)
        wordList = textParse(feed0['entries'][i]['title'].split('<')[0])
        docList.append(wordList)
        classList.append(0)
        fullText.extend(wordList)
    vocabList=createVocabList(docList)

    top30Words=calcMostFreq(vocabList,fullText)
    for pairW in top30Words:
        if pairW[0] in vocabList: vocabList.remove(pairW[0])

    trainingSet=list(range(minLen*2));testSet=[]
    for i in range(int(minLen*0.2)):
        randIndex=int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat=[];trainClasses=[]
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam=trainNB0(trainMat,trainClasses)
    errorCount=0.0
    errorList=set()
    for docIndex in testSet:
        wordVector=setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount+=1.0
            errorList|=set(docList[docIndex])
    # if(len(errorList)>0):print("classification error", errorList)
    print('the error rate is: %f'%(errorCount/len(testSet)))
    return vocabList,p0V,p1V

def getTopWords(ny,sf):
    vocabList,p0V,p1V=localWords(ny,sf)
    topNY=[];topSF=[]
    for i in range(len(p0V)):
        if(p0V[i]>-2.0): topSF.append((vocabList[i],p0V[i]))
        if (p1V[i] > -2.0): topNY.append((vocabList[i], p1V[i]))
    sortedSF=sorted(topSF,key=lambda x:x[1],reverse=True)
    print("*LW**LW**LW**LW**LW**LW**LW**LW**LW**LW**LW*")
    for item in topSF:
        print(item[0])
    sortedNY = sorted(topNY, key=lambda x: x[1], reverse=True)
    print("*ML**ML**ML**ML**ML**ML**ML**ML**ML**ML**ML*")
    for item in topNY:
        print(item[0])

# ML=feedparser.parse('https://www.profgalloway.com/feed/')
# LW=feedparser.parse('https://www.lesswrong.com/feed.xml?view=curated-rss')

