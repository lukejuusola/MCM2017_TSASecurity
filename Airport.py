import random
import numpy as np

class Airport:
    class Queue:
        def __init__(self, exitRates, output):
            """exitRates: probability array
               output: output Holder class"""
            self.size = 0
            self.holder = 0
            self.exitRates = exitRates
            self.output = output
            self.avg = np.average(exitRates)
        
        def add(self, num):
            if size == 0:
                self.holder = random.choice(exitRates)
            self.size += num

        def tick(self, num):
            self.holder -= num
            if self.holder <= 0:
                if size > 0:
                    if output.add():
                        size -= 1
                        self.holder = random.choice(exitRates)

        def waittime(self, num):
            return self.size * self.avg

    class Holder:
        def __init__(self, capacity, waits, outputs, decision):
            """decision is a function"""
            self.spots = np.full(capacity, np.NaN)
            self.waits = waits
            self.outputs = outputs
            self.outrates = outrates

        def add(self, num):           
            i = np.where(self.spots < 0)
            if len(i) > 0:
                self.spots[i[0][0]] = random.choice(waits)
                return True
            else:
                return False

        def tick(self, num):
            self.spots -= num
            numout = len(np.where(self.spots < 0)[0])
            self.spots[self.spots < 0] = np.NaN
            outwaits = [output.waittime() for output in outputs]
            for i in range(0 numout):
                outi = decision(outwaits)
                
                
            
            
            
            
