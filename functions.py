import numpy as np

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

def loadData(location):
    fnames = np.genfromtxt(location+'/info.dat', dtype=type(''), delimiter=',')
    data = []
    for ftype, name in fnames:
        data.append((ftype, np.loadtxt(location + '/' + name + '.dat', delimiter=',')))    
    return data

def makeaaronsdata(fullspots):
    filled = np.zeros(len(fullspots[0]))
    lastnans = np.isnan(fullspots[0])
    data = []
    for row in fullspots:
        size = len([row > 0])
        notnans = ~np.isnan(row)
        vadded = row[np.multiply(notnans, lastnans)]
        lastnans = np.isnan(row)
        data.append(vadded)
    return np.array(data)
        
    
