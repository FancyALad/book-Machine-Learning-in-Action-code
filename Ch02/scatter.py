import matplotlib
import kNN
from numpy import *
datingDataSet,datingLabels=kNN.file2matrix("datingTestSet2.txt")
import matplotlib.pyplot as plt
fig=plt.figure()
ax=fig.add_subplot(111)

scatter=ax.scatter(datingDataSet[:,1],datingDataSet[:,2],15.0*array(datingLabels),15.0*array(datingLabels),)

plt.show()
plt.pause(0.01)