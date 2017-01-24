import numpy as np
from holder import Holder
from queue  import Queue
from airport import Airport
from exit import Exit
from split import Split
from merge import Merge
from decision import Decision
import matplotlib.pyplot as plt
from functions import *
import math

numID = 4
cap2 = 16
capbagin = 5*6
capbagout = 10*6
cap3 = 10*6
mergecap = 10

dropoffsize = 4*16
pickupsize = 4*16
mmwavesize = 1*6
xraysize = 1*6
leavetimes = [1,2,2,3]

bagdist = [1,1,2]
idTimes = np.genfromtxt('distributions/idCheck.csv', delimiter=',').astype(int)
mmwavetimes = np.genfromtxt('distributions/mmScan.csv', delimiter=',').astype(int)
pickuptimes = np.genfromtxt('distributions/pickupTimes.csv', delimiter=',').astype(int)
dropofftimes = pickuptimes
xraytimes = np.genfromtxt('distributions/xray.csv', delimiter=',').astype(int)
bagtimes = np.random.normal(5, 1, 100000).astype(int)
servicetimes = np.random.normal(50, 10, 100000).astype(int)
serviceutility = np.random.normal(1, 0.1, 100000)
storemax = 50

def timeFunc(t):
    return 1

if __name__ == '__main__':
    lobby = Holder(8000, leavetimes, name='lobby')
    store1 = Queue(servicetimes, capacity=storemax, name='store1')
    store2 = Queue(servicetimes, capacity=storemax, name='store2')
    store1.setUtility(serviceutility)
    store2.setUtility(serviceutility)
    qIn = Queue(leavetimes, name='qIn')
    dropoffA = Holder(dropoffsize, dropofftimes, name='dropoffA')
    q3a = Queue(leavetimes, capacity=cap3, name='q3a')
    bagAin = Queue(bagtimes, capacity=capbagin, name='bagAin')
    bagAin.ptype = 'bag'
    xrayA = Holder(xraysize, xraytimes, name='xrayA')
    xrayA.ptype = 'bag'
    mmwaveA = Holder(mmwavesize, mmwavetimes, name='mmwaveA')
    idcheck = Holder(numID, idTimes, name='idcheck')
    pickupA = Holder(pickupsize, pickuptimes, name='pickupA')
    ext = Exit()
    d1 = Decision([2],[qIn, store1, store2], calcprob, name='d1')
    sA = Split(q3a, bagAin, bagdist, name='sA')
    mA = Merge(mergecap, int(mergecap*max(bagdist)), 'normal', 'bag', pickupA, sA, name='mA')

    objects = [lobby, store1, store2, d1, qIn, idcheck, dropoffA, sA,q3a,  mmwaveA,bagAin, xrayA, mA,pickupA,  ext]
    edgelist = [(lobby, d1), (d1, qIn), (d1, store1), (d1, store2), (store1, lobby), (store2, lobby), (qIn, dropoffA), (dropoffA, sA), (sA, q3a), (sA,bagAin), (bagAin, xrayA), (xrayA, mA), (q3a,mmwaveA),(mmwaveA, idcheck), (idcheck, mA), (mA, pickupA),  (pickupA, ext) ]
    adjmatrix = edgeToAdj(objects, edgelist)
    ap = Airport(0, len(objects)-1, objects, adjmatrix)
