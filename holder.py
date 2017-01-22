import numpy as np

class Holder:
        def __init__(self, capacity, exitRates):
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

        def add(self, num):
                '''Attemps to add num people to the holder. Returns the number of
                people rejected from the holder.'''
                i = np.where(np.isnan(self.spots))[0]
                if len(i) > num:
                        self.spots[i[0:num]] = self.exitRates[np.random.randint(0, len(self.exitRates), num)]
                        return 0
                else:
                        self.spots[i] = self.exitRates[np.random.randint(0, len(self.exitRates), len(i))]
                        return num - len(i)

        def getsize(self):
                '''Returns the number of spots that are full'''
                return len(np.where(self.spots > 0)[0])

        def getData(self):
                return ', '.join(self.spots.astype(str))

        def isSpace(self):
                return self.getsize() < self.capacity

        def tick(self, num):
                '''Updates the holder array for num ticks.'''
                self.spots -= num
                leaving = np.where(self.spots <= 0)[0]
                numLeaving = len(leaving)
                if numLeaving > 0:
                        left = numLeaving - self.output.add(numLeaving)
                        self.spots[leaving[0:left]] = np.NaN

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
