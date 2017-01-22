import numpy as np
from holder import Holder
from queue  import Queue
from airport import Airport
from exit import Exit
from decision import Decision
import matplotlib.pyplot as plt

ALPHA = 1

def calcprob(outputs):
    #print(outputs)
    u = np.array([0.0] * len(outputs))
    exitTimes = []
    for out in outputs:
        exitTimes.append(out.exitWait())
    exitTimes = np.array(exitTimes)
    mintime = np.min(exitTimes)
    for i in range(0, len(u)):
        u[i] = outputs[i].utility - ALPHA * (exitTimes[i] - mintime)
    u -= np.min(u) - 1
    for i in range(0, len(u)):
        u[i] *= outputs[i].isSpace()
    prob = (u ** 2)
    if np.sum(prob) == 0:
        return prob
    prob = prob / np.sum(prob)
    return prob
    
def edgeToAdj(objects, edgeList):
        s = len(objects)
        adjacency = np.zeros((s,s))
        for e in edgeList:
                for o in range(len(objects)):
                        if objects[o] == e[0]:
                                i = o
                        if objects[o] == e[1]:
                                j = o
                adjacency[i,j] = 1
        return adjacency

def timeFunc(t):
    x = np.sin(t/1000)*1.01
    x = max(0, x)
    x = int(x)
    return x

def loadData(location):
    fnames = np.genfromtxt(location+'/info.dat', dtype=type(''), delimiter=',')
    data = []
    for ftype, name in fnames:
        data.append((ftype, np.loadtxt(location + '/' + name + '.dat', delimiter=',')))    
    return data

if __name__ == '__main__':
    q1 = Queue([1])
    h1 = Holder(1, np.random.normal(100, 5, 100000).astype(int))
    h2 = Holder(1, np.random.normal(100, 5, 100000).astype(int))
    h3 = Holder(1, np.random.normal(100, 5, 100000).astype(int))
    d1 = Decision([0,1,2], [h1, h2, h3], calcprob)
    out = Exit()
    objects = [q1, d1, h1, h2, h3, out]
    edgelist = [(q1, d1), (d1,h1),(d1,h2),(d1,h3),(h1,out),(h2,out),(h3,out)]
    adjmatrix = edgeToAdj(objects, edgelist)
    ap = Airport(0, len(objects)-1, objects, adjmatrix)
    



