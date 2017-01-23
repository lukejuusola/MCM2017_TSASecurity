import random
import numpy as np
from scipy.sparse.csgraph import breadth_first_order
import os
                
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
                return np.array([x.getsize() for x in self.parts])

        def exitWait(self):
                '''Need to create a minimum exitWait function.'''
                return self.start.exitWait()

        def run(self, numTicks, resolution, timeFunc, outname='none'):
                '''Run the airport for numTicks ticks using timeFunc to determine
                how many people enter the airport on a given tic, where timeFunc
                is of the form numEnteringOnTick = timeFunc(tick). To save data, outname
                should be the target filepath. Otherwise, outname = 'none' '''
                if outname != 'none' and not os.path.exists(outname):
                        os.makedirs(outname)
                finfo = open(outname + '/info.csv', 'w')
                t = 0
                if outname != 'none':
                        fouts = []
                        for obj in self.parts:
                                finfo.write(str(obj) + ',' + hex(id(obj)) + '\n')
                                fouts.append(open(outname + '/' +  hex(id(obj)) + '.csv','w'))
                finfo.close()
                while t < numTicks:
                        self.start.add(timeFunc(t))
                        self.tick(resolution)
                        sizes = self.getSizes()
                        if (outname != 'none'):
                                for i in range(0, len(self.parts)):
                                        fouts[i].write(self.parts[i].getData() + '\n')
                        t += resolution
                if outname != 'none':
                        for f in fouts:
                                f.close()
                

        def clear(self):
                for p in self.parts:
                        p.clear()



