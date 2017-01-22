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

        def getData(self):
                return str(self.size);

        def clear(self):
                return None
