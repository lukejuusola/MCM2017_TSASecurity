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
