import numpy as np
import csv

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

def chooseLeast(outputs):
        u = np.array([0.0] * len(outputs))
        exitTimes = []
        for out in outputs:
                exitTimes.append(out.exitWait())
        mini = exitTimes.index(min(exitTimes))
        u[mini] = 1
        if not outputs[mini].isSpace():
                u[mini] = 0
        return u
                
                

def loadData(location):
    fnames = np.genfromtxt(location+'/info.dat', dtype=type(''), delimiter=',')
    data = []
    for ftype, name in fnames:
        data.append((ftype, np.loadtxt(location + '/' + name + '.dat', delimiter=',')))    
    return data

def makeData(fullspots):
    filled = np.zeros(len(fullspots[0]))
    lastnans = np.isnan(fullspots[0])
    data = []
    for row in fullspots:
        size = len([row > 0])
        notnans = ~np.isnan(row)
        vadded = row[np.multiply(notnans, lastnans)]
        lastnans = np.isnan(row)
        data.append(vadded)
    return data
        
def getNames(loc):
    f = open(loc)
    names = []
    for line in f:
        names.append(line.split(',')[1].strip())
    return names

def loadData(location):
        data = []
        f = open(location, 'r')
        r = csv.reader(f, delimiter=",")
        for row in r:
                row = np.array(row)
                data.append(row)
        return data

def getCol(i, arr):
        x = []
        for a in arr:
                x.append(a[i])
        return x

def loadFromFile(dirname):
        finfo = open(dirname + '/info.dat')
        data = []
        for line in finfo:
                ptype, name = line.split(',')
                location = dirname + '/' + name.strip() + '.dat'
                data.append(loadData(location))
        return data
