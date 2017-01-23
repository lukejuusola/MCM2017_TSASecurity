import numpy as np

class Merge:
    def __init__(self, capacity, bcapacity, typeA, typeB, output, split,  name=''):
        self.typeA = typeA
        self.typeB = typeB
        self.output = output
        self.split = split
        self.numAwaiting = 0
        self.numBwaiting = 0
        self.numlastleft = 0
        self.capacity = capacity
        self.bcapacity = bcapacity
        self.name = name
        if self.name == '':
            self.name = hex(id(self))
        
    def add(self, num, ptype='normal'):
        if ptype == self.typeA:
            if num + self.numAwaiting > self.capacity:
                num -= self.capacity - self.numAwaiting
                self.numAwaiting = self.capacity
                return num
            else:
                self.numAwaiting += num
        if ptype == self.typeB:
            length = min(len(self.split.numvalues), self.capacity)
            if self.numBwaiting > self.bcapacity:
                num -= self.bcapacity - self.numBwaiting
                self.numBwaiting = self.bcapacity
                return num
            else:
                self.numBwaiting += num
        return 0

    def tick(self, num):
        self.numlastleft = 0
        while self.numAwaiting > 0 and self.numBwaiting >= self.split.numvalues[0]:
            if self.output.add(1) > 0:
                break
            self.numBwaiting -= self.split.numvalues[0]
            self.numAwaiting -= 1
            self.numlastleft += 1
            del self.split.numvalues[0]

    def getsize(self):
        return 0

    def getData(self):
        ll = self.numlastleft
        self.numlastleft = 0
        '''returns string in the form A waiting, B waiting, lastleft'''
        return str(self.numAwaiting) + ',' + str(self.numBwaiting) + ',' + str(ll)

    def exitWait(self):
        return self.output.exitWait()

    def clear(self):
        self.numAwaiting = 0
        self.numBwaiting = 0
        self.numlastleft = 0
    
