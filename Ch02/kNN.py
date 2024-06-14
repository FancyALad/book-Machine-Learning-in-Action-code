from numpy import *
import operator
from os import listdir

def createDataSet():
    group=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    sortedDistIndicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.items(),key=lambda x:x[1],reverse=True)
    return sortedClassCount[0][0]

def file2matrix(filename):
    fr=open(filename)
    arrayOLines=fr.readlines()
    numberOfLines=len(arrayOLines)
    returnMat=zeros((numberOfLines,3))
    classLabelVector=[]
    index=0
    for line in arrayOLines:
        line=line.strip()
        listFromLine=line.split('\t')
        returnMat[index,:]=listFromLine[:3]
        classLabelVector.append(int(listFromLine[-1]))
        index+=1
    return returnMat,classLabelVector

def autoNorm(dataSet):
    minVals=dataSet.min(0)
    maxVals=dataSet.max(0)
    ranges=maxVals-minVals
    normDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normDataSet=dataSet-tile(minVals,(m,1))
    normDataSet=normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

def datingClassTest():
    hoRatio=0.1
    datingDataSet,datingLabels=file2matrix("datingTestSet2.txt")
    norm,ranges,minvals=autoNorm(datingDataSet)
    numTestVecs=int(hoRatio*datingDataSet.shape[0])
    errorcount=0.0
    for i in range(numTestVecs):
        classResult=classify0(norm[i,:],norm[numTestVecs:,:],datingLabels[numTestVecs:],3)
        print("the classifier came back with %d, the real answer is %d"\
              %(classResult,datingLabels[i]))
        if(classResult!=datingLabels[i]):
            errorcount+=1.0
    print("the total error rate is %f"%(errorcount/float(datingDataSet.shape[0])))

def classifyPerson():
    resultList=['不喜欢','一般喜欢','很喜欢']
    percentTats=float(input("玩游戏所消耗时间百分比："))
    ffMiles=float(input("飞行里程数："))
    iceCream=float(input("每周消耗冰淇淋公升数："))
    datingDataSet,datingLabels=file2matrix("datingTestSet2.txt")
    normDataSet,ranges,minVals=autoNorm(datingDataSet)
    inArr=array([ffMiles,percentTats,iceCream])
    ClassResult=classify0((inArr-minVals)/ranges,normDataSet,datingLabels,3)
    print("你很可能%s这个人"%resultList[ClassResult-1])

def img2vector(filename):
    fr=open(filename)
    returnVector=zeros((1,1024))
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVector[0,32*i+j]=int(lineStr[j])
    return returnVector

def handwritingDigitsTest():
    trainSetLabels=[]
    trainingFlieList=listdir("trainingDigits")
    trainSetSize=len(trainingFlieList)
    trainingSet=zeros((trainSetSize,1024))
    for i in range(trainSetSize):
        theLabel=trainingFlieList[i].split('.')[0]
        trainSetLabels.append(int(theLabel.split('_')[0]))
        trainingSet[i,:]=img2vector("trainingDigits/%s"%trainingFlieList[i])
    testFileList=listdir("testDigits")
    testListLen=len(testFileList)
    errorCount=0.0
    for i in range(testListLen):
        testFileName=testFileList[i]
        testFile=testFileName.split('.')[0]
        testLabel=int(testFile.split('_')[0])
        inArr=img2vector("testDigits/%s"%testFileName)
        classResult=classify0(inArr,trainingSet,trainSetLabels,3)
        print("the classifier came back with %d, the real answer is %d"%(classResult,testLabel))
        if(classResult!=testLabel): errorCount+=1.0
    print("the error rate is %f"%(errorCount/testListLen))

