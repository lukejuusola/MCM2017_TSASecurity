import random
import numpy as np
from scipy.sparse.csgraph import breadth_first_order

class Queue:
        def __init__(self, exitRates):
                '''
                exitRates: probability array
                output: output Holder class
                '''
                self.size = 0
                self.holder = 0
                self.exitRates = exitRates
                self.output = None
                self.avg = np.average(exitRates)
                self.utility = [0]
                
        def add(self, num):
                '''Attemps to add num people to the queue. Returns the number of
                people rejected from the queue. No one should be rejected.'''
                if self.size == 0:
                        self.holder = random.choice(self.exitRates)
                self.size += num
                return 0

        def getsize(self):
                '''Return size'''
                return self.size

        def tick(self, num):
                '''Updates the queue by num ticks.'''
                while(num > 0 and self.size > 0):
                        temp = num
                        num -= self.holder
                        self.holder -= temp
                        if self.holder <= 0:
                                if self.output.add(1) == 0:
                                        self.size -= 1
                                        self.holder = random.choice(self.exitRates)
                                else:
                                        break

        def exitWait(self):
                '''Returns the expected exitWait of the queue.'''
                return (self.size + 1) * self.avg + self.output.exitWait()
                
        def selfWait(self):
                return (self.size + 1) * self.avg

        def utility(self):
                return random.choice(self.utility)
                        
        def setUtility(self, u):
                self.utility = u

        def clear(self):
                self.size = 0
                self.holder = 0

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
                self.utility = [0]

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

        def tick(self, num):
                '''Updates the holder array for num ticks.'''
                self.spots -= num
                leaving = np.where(self.spots <= 0)[0]
                numLeaving = len(leaving)
                if numLeaving > 0:
                        left = numLeaving - self.output.add(numLeaving)
                        self.spots[leaving[0:left]] = np.NaN

        def utility(self):
                return random.choice(self.utility)

        def setUtility(self, u):
                self.utility = u
                        
        def exitWait(self):
                '''The expected exitWait of a holder.'''
                return self.avg + self.output.exitWait()
                
        def selfWait(self):
                return self.avg

        def clear(self):
                self.spots = np.full(len(self.spots), np.NaN)

class Decision:
        def __init__(self, exits, output, func):
                """Exits is a list of INDEXES"""
                self.output = output
                self.func = func
                self.exits = exits

        def add(self, num):
                while num > 0:
                        prob = self.func(self.output)
                        if np.sum(prob) == 0:
                                return num
                        if np.random.choice(self.output, p=prob).add(1) > 0:
                                print('WE #&%$ED UP')
                        num -= 1
                return 0

        def getsize(self):
                return 0

        def tick(self, num):
                return 0

        def exitWait(self):
                exitWait = 0
                prob = self.func(self.output)
                for i in self.exits:
                        exitWait += self.output[i].exitWait() * prob[i]
                return exitWait

        def clear(self):
                return None
"""
class Decision:
        def __init__(self, alphas, betas):
                '''Outputs is a list of objects the decision is outputting to.
                The probability of traveling to outputs[i] is 
                alphas[i]*outputs[i].exitWait()+betas[i]. exits are the indices
                of outputs which lead through security.'''
                self.outputs = None
                self.alphas = alphas
                self.betas = betas
                self.exits = None
                self.probabilities = [0]*len(alphas)
                
        def add(self, num):
                '''Attemps to add num people to the decision. Returns the number of
                people rejected from the decision. No one should be rejected.'''
                while num > 0:
                        outloc = np.random.choice(self.output, p=self.probabilities)
                        if outloc.add(1) == 0:
                                num -= 1
                        else:
                                self.tick(1)
                                if np.sum(self.probabilities) == 0:
                                        return num
                return 0
                        
        def tick(self, num):
                '''Updates the decision probabilities on the current tick.'''
                for i in range(len(self.output)):
                        self.probabilities[i] = self.alphas[i]*self.output[i].exitWait() + self.betas[i]
                
        def exitWait(self):
                exitWait = 0
                for i in self.exits:
                        exitWait += self.output[i].exitWait()*self.probabilities[i]
                return exitWait                      
        """

class Exit:
        def __init__(self):
                self.output = None
                self.size = 0
                
        def tick(self, num):
                return None
                
        def add(self, num):
                self.size += num
                return 0

        def getsize(self):
                return self.size
        
        def exitWait(self):
                return 0

        def clear(self):
                return None
                
class Airport:
        '''Airport tick must operate so that decisions are updated last.'''
        def __init__(self, start, end, parts, adjacency):
                '''
                start: The starting object for the airport.
                queues: the list of all queues
                holders: the list of all holders
                decisions: the list of all decisions
                '''
                self.start = parts[start]
                self.end = parts[end]
                self.parts = np.array(parts)
                self.adjacency = np.array(adjacency)
                
                for i in range(len(parts) - 1):
                        outputs = self.parts[np.where(adjacency[i] == 1)[0]]
                        if len(outputs) == 1:
                                self.parts[i].output = outputs[0]
                        else:
                                self.parts[i].output = outputs
                self.updateOrder = breadth_first_order(np.transpose(self.adjacency),end)
                
        def tick(self, num):
                '''Tick update the queues, holders and decisions in the airport.
                Updates are done in order from the beginning of the airport to the
                end.'''
                for i in self.updateOrder[0]:
                        self.parts[i].tick(num)

        def getSizes(self):
                return np.array([x.getsize() for x in ap.parts])

        def exitWait(self):
                '''Need to create a minimum exitWait function.'''
                return self.start.exitWait()

        def run(self, numTicks, resolution, timeFunc):
                '''Run the airport for numTicks ticks using timeFunc to determine
                how many people enter the airport on a given tic, where timeFunc
                is of the form numEnteringOnTick = timeFunc(tick)'''
                t = 0
                while t < numTicks:
                        self.start.add(timeFunc(t))
                        self.tick(resolution)
                        sizes = self.getSizes()
                        print(str(sizes) + '\t' + str(np.sum(sizes)))
                        t += resolution

        def clear(self):
                for p in parts:
                        parts.clear()

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


lobby = Holder(100, [1,2,2,3,3,3,4,4,5])
q1 = Queue([1])
q2 = Queue([1])
q3 = Queue([1])
h1 = Holder(10, [15,10])
h2 = Holder(10, [15,10])
h3 = Holder(10, [15,10])
gates = Exit()

def f1(outputs):
        a = [1 / len(outputs)] * len(outputs)
        return np.array(a)
d1 = Decision([0,1,2], [q1, q2, q3], f1)
objects = [lobby, q1, q2, q3, h1, h2, h3, d1, gates]

edgeList = [(lobby,d1),(d1, q1),(d1,q2),(d1,q3),(q1,h1),(q2,h2),(q3,h3),(h1,gates),(h2,gates),(h3,gates)]
adjacency = edgeToAdj(objects, edgeList)
ap = Airport(0, 8, objects, adjacency)

def timeFunc(t):
        return np.random.choice([2])
'''
ticks = 0
while (ticks < 10 ** 6):
        ticks += 1
        if ticks % 2 == 0:
                ap.parts[0].add(1)
        ap.tick(1)
        if(ticks % 10 ** 5 == 0):
                print('1: ' + str(ap.parts[0].spots))
                print('2: ' + str(ap.parts[1].size))
                print('3: ' + str(ap.parts[4].spots))
                print('\n')
'''
        
"""        

gates = Exit()

pickupER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
pickup0 = Queue(pickupER)
pickup1 = Queue(pickupER)
pickup2 = Queue(pickupER)
pickupPC = Queue(pickupER)
pickup = [pickup0, pickup1, pickup2, pickupPC]

idScanER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
idScan0 = Queue(idScanER)
idScan1 = Queue(idScanER)
idScan2 = Queue(idScanER)
idScanPC = Queue(idScanER)
idScan = [idScan0, idScan1, idScan2, idScanPC]

unpackER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
unpackSize = 4
unpack0 = Holder(unpackSize, unpackER)
unpack1 = Holder(unpackSize, unpackER)
unpack2 = Holder(unpackSize, unpackER)
unpackPC = Holder(unpackSize, unpackER)
unpack = [unpack0, unpack1, unpack2, unpackPC]

securityER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
security0 = Queue(securityER)
security1 = Queue(securityER)
security2 = Queue(securityER)
securityPC = Queue(securityER)
security = [security0, security1, security2, securityPC]

tsaOuts = [security0, security1, security2, securityPC]
tsaA = [0,0,0,0]
tsaB = [.25,.25,.25,.25]
tsaExits = [0,1,2,3]
tsa = Decision(tsaA, tsaB)

hall1Size = 10**4
hall1ER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
hall1 = Holder(hall1Size, hall1ER)

shopER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
shop0 = Queue(shopER)
shop1 = Queue(shopER)
shop2 = Queue(shopER)
shop3 = Queue(shopER)
shops = [shop0, shop1, shop2, shop3]

shopsOuts = [shop0, shop1, shop2, shop3, hall1]
shopsA = [0,0,0,0,0]
shopsB = [.2,.2,.2,.2,.2]
shopsExits = [4]
lobby = Decision(shopsA, shopsB)

for s in shops:
        s.output = lobby

hall0Size = 10**4
hall0ER = [2,3,3,3,4,4,4,4,4,5,5,5,5,5,5,6,6,6,6,6,7,7,7,8]
hall0 = Holder(hall0Size, hall0ER)

queues = shops + security + idScan + pickup
holders = unpack + [hall0, hall1]
decisions = [tsa, lobby]

adjacency = np.loadtxt("adjacency.csv", delimiter=',')
parts = queues + holders + decisions + [gates]
#hall0 is the 20th element
ap = Airport(20, parts, adjacency)

ap.tick(1)"""

