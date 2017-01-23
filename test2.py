import numpy as np
from holder import Holder
from queue  import Queue
from airport import Airport
from exit import Exit
from split import Split
from merge import Merge
from decision import Decision
import matplotlib.pyplot as plt
from functions import *

ALPHA = 1

def calcprob(outputs):
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

def timeFunc(t):
    x = np.sin(t/1000)*1.01
    x = max(0, x)
    x = int(x)
    return x

def genConstFunc(alpha):
    def constFunc(t):
        return alpha
    return constFunc

def genLinFunc(alpha):
    def f(t):
        rate = alpha*t
        return int(rate) + np.random.choice([0,1],p=[1-(rate-int(rate)), (rate-int(rate))])
    return f

if __name__ == '__m!ain__':
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

if __name__ == '__main__':
    inq = Queue(np.random.normal(13, 4.5, 100000).astype(int))
    h1 = Holder(100, np.random.normal(10, 2, 100000).astype(int))
    q1 = Queue(np.random.normal(15, 2, 100000).astype(int), capacity=20)
    q2 = Queue(np.random.normal(5, 2, 100000).astype(int), capacity=10)
    q2.ptype = 'bags'
    h2 = Holder(5, np.random.normal(5, 2, 100000).astype(int))
    out = Exit()
    split = Split(q1, q2, [2])
    merge = Merge(1, 'normal', 'bags', out, split)
    objects = [inq, h1, q1, q2, split, merge, h2, out]
    edgelist = [(inq, h1),(h1, split), (split, q1), (split, q2), (q1, merge), (q2, merge), (merge, h2), (h2,out)]
    adjmatrix = edgeToAdj(objects, edgelist)
    ap = Airport(0, len(objects)-1, objects, adjmatrix)
    



