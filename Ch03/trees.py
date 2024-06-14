from math import log
from importlib import reload

def calcShannonEnt(dataSet):
    numEntries=len(dataSet)
    labelCounts={}
    for featVecs in dataSet:
        labelCounts[featVecs[-1]]=labelCounts.get(featVecs[-1],0)+1
    shannonEnt=0.0
    for key in labelCounts:
        prob=labelCounts[key]/numEntries
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def createDataSet():
    dataSet=[[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels=['no surfacing','flippers']
    return dataSet,labels

def splitDataSet(dataSet,axis,value):
    retDataSet=[]
    for featVec in dataSet:
        if featVec[axis]==value:
            reducedFeatVec=featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures=len(dataSet[0])-1
    baseEntropy=calcShannonEnt(dataSet)
    bestInfoGain=0.0;bestFeature=-1
    for i in range(numFeatures):
        featList=[example[i] for example in dataSet]
        uniqueFeature=set(featList)
        newEntropy=0.0
        for value in uniqueFeature:
            subDataSet=splitDataSet(dataSet,i,value)
            prob=len(subDataSet)/float(len(dataSet))
            newEntropy+=prob*calcShannonEnt(subDataSet)
        infoGain=baseEntropy-newEntropy
        if infoGain>bestInfoGain:
            bestInfoGain=infoGain
            bestFeature=i
    return bestFeature

def majorityCnt(classList):
    classCount={}
    for vote in classList:
        classCount[vote]=classCount.get(vote,0)+1
    sortedClassCnt=sorted(classCount.items(),key=lambda x:x[1],reverse=True)
    return sortedClassCnt[0][0]

def createTree(dataSet,labels):
    classList=[i[-1] for i in dataSet]
    if len(set(classList))==1: return classList[0]
    if len(dataSet[0])==1: return majorityCnt(classList)
    bestFeature=chooseBestFeatureToSplit(dataSet)
    bestLabel=labels[bestFeature]
    myTree={bestLabel:{}}
    del(labels[bestFeature])
    featValues=[i[bestFeature] for i in dataSet]
    uniqueVals=set(featValues)
    subLabel = labels[:]
    for value in uniqueVals:
        subLabel = labels[:]
        myTree[bestLabel][value]=createTree(splitDataSet(dataSet,bestFeature,value),subLabel)
    return myTree

def classify(inputTree,featLabels,testVec):
    firstStr=list(inputTree.keys())[0]
    secondDict=inputTree[firstStr]
    featIndex=featLabels.index(firstStr)
    for key in list(secondDict.keys()):
        if testVec[featIndex]==key:
            if type(secondDict[key]).__name__=='dict':
                classLabel=classify(secondDict[key],featLabels,testVec)
            else: classLabel=secondDict[key]
    return classLabel

def storeTree(inputTree,filename):
    import pickle
    fw=open(filename,'wb')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr=open(filename,'rb')
    return pickle.load(fr)
