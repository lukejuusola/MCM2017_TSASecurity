import numpy as np

class Split:
    def __init__(self, outA, outB, numdist):
        '''exits is  a list of indices. numdist is the probability distribution of
        the number of "bags" each passenger has. # to outB = numdist * #
        to outA'''
        self.outA = outA
        self.outB = outB
        self.numdist = np.array(numdist)
        self.numvalues = []
        self.lastadded = 0
        self.lastvalues = []

    def add(self, num, ptype='normal'):
        self.lastadded = 0
        self.lastvalues = []
        while num > 0:
            numbags = np.random.choice(self.numdist)
            self.lastvalues.append(numbags)
            self.numvalues.append(numbags)
            if self.outB.isSpace(numbags):
                self.outB.add(numbags, ptype)
            else:
                return num
            if self.outA.add(1, ptype) > 0:
                return num
            self.lastadded += 1
            num -= 1
        return 0

    def tick(self, num):
        return 0

    def getsize(self):
        return 0

    def getData(self):
        self.lastvalues = np.array(self.lastvalues)
        return str(self.lastadded) + ',' + ','.join(self.lastvalues.astype(str))

    def exitWait(self):
        return max(outA.exitWait(), outB.exitWait())

    def clear(self):
        self.lastadded = 0
        self.lastvalues = []
        self.numvalues = []

    
    
