import numpy as np
from holder import Holder
from queue  import Queue
from airport import Airport
from exit import Exit
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
    



