import numpy as np



class Queue:
        def __init__(self, exitRates):
                '''
                exitRates: probability array
                output: output Holder class
                '''
                self.size = 0
                self.holder = 0
                self.exitRates = np.array(exitRates)
                self.output = None
                self.avg = np.average(exitRates)
                self.utility = np.array([0])
                self.lastnumleft = 0
                self.lastnumadded = 0
                
        def add(self, num):
                '''Attemps to add num people to the queue. Returns the number of
                people rejected from the queue. No one should be rejected.'''
                if self.size == 0:
                        self.holder = np.random.choice(self.exitRates)
                self.size += num
                self.lastnumadded = num
                return 0

        def getsize(self):
                '''Return size'''
                return self.size

        def tick(self, num):
                '''Updates the queue by num ticks.'''
                numleft = 0
                while(num > 0 and self.size > 0):
                        temp = num
                        num -= self.holder
                        self.holder -= temp
                        if self.holder <= 0:
                                if self.output.add(1) == 0:
                                        self.size -= 1
                                        numleft += 1
                                        self.holder = np.random.choice(self.exitRates)
                                else:
                                        break
                self.lastnumleft = 0

        def getData(self):
            '''Returns a string containing, in order, size numadded numleft. Should be called
            once per tick'''
            return str(self.size) + ', ' + str(self.lastnumadded) + ', ' + str(self.lastnumleft)
            
        def exitWait(self):
                '''Returns the expected exitWait of the queue.'''
                return (self.size + 1) * self.avg + self.output.exitWait()

        def isSpace(self):
                return 1
                
        def selfWait(self):
                return (self.size + 1) * self.avg

        def utility(self):
                return np.random.choice(self.utility)
                        
        def setUtility(self, u):
                self.utility = np.array(u)

        def clear(self):
                self.size = 0
                self.holder = 0
