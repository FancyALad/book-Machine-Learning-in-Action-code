import matplotlib.pyplot as plt
import matplotlib

decisionNode=dict(boxstyle="sawtooth",fc="0.8") #sawtooth是锯齿形的外框；fc表示facecolor，是填充颜色，还可以有ec(edgecolor)，边线颜色
leefNode=dict(boxstyle="round4",fc="0.8")       #round4是圆滑边角的近似椭圆的四边形边框
arrow_args=dict(arrowstyle="<-")                #“<-”是指向文本框的箭头样式

def plotNode(nodeTxt,centerPt,parentPt,nodeType):
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords='axes fraction',\
                xytext=centerPt,ha="center",bbox=nodeType,arrowprops=arrow_args)
    #xycoords是指定xy参照的坐标系，‘axes fraction’是设置图形中位置范围左下（0，0），右上（1，1）
    #xy是箭头的起始点，xytext是文本的坐标，textcoords可以对xytext实现类似xycoords的效果；参数也可以设置为‘data’，根据值和坐标轴绘制
    #ha是文本的对齐方式，‘center’是居中；bbox是文本框的样式设置，
'''
#初版
def createPlot():
    fig=plt.figure(1,facecolor='white')
    fig.clf()
    createPlot.ax1=plt.subplot(111,frameon=False)
    plotNode('a decision node',(0.5,0.1),(0.5,0.1),decisionNode)
    plotNode('a leaf node',(0.8,0.1),(0.3,0.8),leefNode)
    plt.show()
'''
def getNumLeafs(myTree):
    numLeafs=0
    firstStr=list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in list(secondDict.keys()):
        if type(secondDict[key]).__name__=='dict':
            numLeafs+=getNumLeafs(secondDict[key])
        else: numLeafs+=1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth=0
    firstStr=list(myTree.keys())[0]
    secondDict=myTree[firstStr]
    for key in list(secondDict.keys()):
        if type(secondDict[key]).__name__=="dict":
            thisDepth=1+getTreeDepth(secondDict[key])
        else: thisDepth=1
        maxDepth=maxDepth if maxDepth>thisDepth else thisDepth
    return maxDepth

# 父节点与子节点间的特征值标注
def plotMidText(cntrPt,parentPt,txtString):
    xMid=(parentPt[0]-cntrPt[0])/2+cntrPt[0]
    yMid=(parentPt[1]-cntrPt[1])/2+cntrPt[1]
    createPlot.ax1.text(xMid,yMid,txtString)

def plotTree(myTree,parentPt,nodeTxt):
    numLeafs=getNumLeafs(myTree)
    depth=getTreeDepth(myTree)
    firstStr=list(myTree.keys())[0]
    # cntrPt是每一个非叶节点的定位，plotTree.xOff是对已绘制的叶节点的x轴定位
    cntrPt=(plotTree.xOff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yOff)
    plotMidText(cntrPt,parentPt,nodeTxt)
    plotNode(firstStr,cntrPt,parentPt,decisionNode)
    secondDict=myTree[firstStr]
    plotTree.yOff-=1.0/plotTree.totalD
    for key in list(secondDict.keys()):
        if type(secondDict[key]).__name__=='dict':
            plotTree(secondDict[key],cntrPt,str(key))
        else:
            plotTree.xOff+=1.0/plotTree.totalW
            plotNode(secondDict[key],(plotTree.xOff,plotTree.yOff),cntrPt,leefNode)
            plotMidText((plotTree.xOff,plotTree.yOff),cntrPt,str(key))
    plotTree.yOff+=1.0/plotTree.totalD  # 返回上一层继续绘制

def createPlot(inTree):
    fig=plt.figure(1,facecolor="white")
    fig.clf()
    axprops=dict(xticks=[],yticks=[])
    createPlot.ax1=plt.subplot(111,frameon=False,**axprops)
    plotTree.totalW=float(getNumLeafs(inTree))
    plotTree.totalD=float(getTreeDepth(inTree))
    # 初始时未绘制叶节点，将初值设置在边沿外0.5格，后续绘制叶节点时会先+1格再绘制，0.5格时x轴方向的基本绘制尺度
    plotTree.xOff=-0.5/plotTree.totalW;plotTree.yOff=1.0
    plotTree(inTree,(0.5,1.0),'')
    plt.show()

def retrieveTree(i):
    listOfTrees=[{"no surfacing":\
                      {0:'no',\
                       1:\
                          {'flippers':\
                               {0:'no',\
                                1:'yes'}}}}, \
                 {"no surfacing":\
                      {0:'no',\
                       1: \
                          {'flippers': \
                               {0:\
                                    {'head': \
                                         {0:'no',\
                                          1:'yese'}},\
                                1:'no'}}}}]
    return listOfTrees[i]