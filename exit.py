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
