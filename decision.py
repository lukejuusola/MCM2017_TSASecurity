import numpy as np

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

        def isSpace(self):
                return 1

        def getData(self):
                return '0'
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
