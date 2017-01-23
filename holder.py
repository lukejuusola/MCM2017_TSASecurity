import numpy as np

class Holder:
        def __init__(self, capacity, exitRates, name=''):
                '''
                capacity: The maximum size of the holder
                exitRates: A randomly distributed array of wait values to choose from
                output: The object which the holder outputs to
                '''
                self.spots = np.full(capacity, np.NaN)
                self.exitRates = np.array(exitRates)
                self.output = None
                self.avg = np.average(exitRates)
                self.utility = np.array([0])
                self.capacity = capacity
                self.ptype = 'normal'
                self.lastvalues = []
                self.lastnumleft = 0
                self.name = name
                if self.name == '':
                        self.name = hex(id(self))

        def add(self, num, ptype='normal'):
                '''Attemps to add num people to the holder. Returns the number of
                people rejected from the holder.'''
                i = np.where(np.isnan(self.spots))[0]
                if len(i) > num:
                        lv = self.exitRates[np.random.randint(0, len(self.exitRates), num)]
                        self.spots[i[0:num]] = lv
                        self.lastvalues = np.append(self.lastvalues, lv).astype(int)
                        return 0
                elif len(i) > 0:
                        lv = self.exitRates[np.random.randint(0, len(self.exitRates), len(i))]
                        self.spots[i] = lv
                        self.lastvalues = np.append(self.lastvalues, lv).astype(int)
                        return num - len(i)
                else:
                        return num

        def getsize(self):
                '''Returns the number of spots that are full'''
                return len(np.where(~np.isnan(self.spots))[0])

        def getData(self):
                lv = self.lastvalues
                ln = self.lastnumleft
                self.lastvalues = []
                self.lastnumleft = 0
                if len(lv) == 0:
                        return str(self.getsize()) + ',' + str(ln)
                else:
                        return str(self.getsize()) + ',' + str(ln) + ',' + ','.join(lv.astype(str))

        def isSpace(self, num=1):
                return self.getsize() + num <= self.capacity

        def tick(self, num):
                '''Updates the holder array for num ticks.'''
                self.spots -= num
                leaving = np.where(self.spots <= 0)[0]
                self.spots[leaving] = 1
                numLeaving = len(leaving)
                left = 0
                if numLeaving > 0:
                        left = numLeaving - self.output.add(numLeaving, ptype=self.ptype)
                        self.spots[leaving[0:left]] = np.NaN
                self.lastnumleft = left

        def utility(self):
                return np.random.choice(self.utility)

        def setUtility(self, u):
                self.utility = np.array(u)
                        
        def exitWait(self):
                '''The expected exitWait of a holder.'''
                return self.selfWait() + self.output.exitWait()
                
        def selfWait(self):
                if self.isSpace():
                        return self.avg
                else:
                        return self.avg + np.average(self.spots)

        def clear(self):
                self.spots = np.full(len(self.spots), np.NaN)
