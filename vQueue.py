import numpy as np
import csv

class vQueue:
	def __init__(self, length, width, initX, initY, separation, orientation, numTurns, file, walkSpeed=5):
		'''
		length: The size of each corridor/turn in the queue
		width: The size of each turn/corridor in the queue
		initX: The x value where people in the queue are serviced
		initY: The y value where people in the queue are serviced
		separation: The minimum distance between people in the queue
		orientation: The orientation of the line. True means vertical, False means horizontal.
		'''
		
		self.length = length
		self.width = width
		self.initX = initX
		self.initY = initY
		self.separation = separation
		self.orientation = orientation
		self.walkSpeed = walkSpeed
		
		self.data = []
		file = open(file, 'r')
		r = csv.reader(file, delimiter=",")
		for row in r:
			row = np.array(row).astype(int)
			self.data.append(row)
			
		self.numTurns = numTurns
		self.counter = 0
		
		#Create the vertical/horizontal x and y values for a snaking queue
		self.xV = np.array([self.initX]*abs(self.length))
		self.yV = np.array(range(self.initY, self.initY+self.length, np.sign(self.length)))
		self.xH = np.array(range(self.initX, self.initX+self.width, np.sign(self.width)))
		self.yH = np.array([self.initY]*abs(self.width))
		
		#Initialize a snaking queue with one turn
		self.x = np.array([])
		self.y = np.array([])
		self.updateLine(numTurns)
		self.spots = np.array([], dtype="int")

		
	def updateLine(self, numTurns):
		self.x = np.array([])
		self.y = np.array([])
		self.numTurns = numTurns
		
		if numTurns == 0:
			if self.orientation:
				self.x = self.xV
				self.y = self.yV
			else:
				self.x = self.xH
				self.y = self.yH
				
		for n in range(0, numTurns, 2):
			if self.orientation:
				self.x = np.append(self.x, self.xV + n*self.width)
				self.y = np.append(self.y, self.yV)
			
				self.x = np.append(self.x, self.xH + n*self.width)
				self.y = np.append(self.y, self.yH + self.length)
				
				self.x = np.append(self.x, self.xV + (n+1)*self.width)
				self.y = np.append(self.y, self.yV[::-1])
				
				self.x = np.append(self.x, self.xH + (n+1)*self.width)
				self.y = np.append(self.y, self.yH)
			else:
				self.x = np.append(self.x, self.xH)
				self.y = np.append(self.y, self.yH + n*self.length)
				
				self.x = np.append(self.x, self.xV + self.width)
				self.y = np.append(self.y, self.yV + n*self.length)
			
				self.x = np.append(self.x, self.xH[::-1])
				self.y = np.append(self.y, self.yH + (n+1)*self.length)
				
				self.x = np.append(self.x, self.xV)
				self.y = np.append(self.y, self.yV + (n+1)*self.length)
		
	def add(self, num):
		if len(self.spots) == 0 and num > 0:
			self.spots = np.array([0])
			num -= 1
		while num > 0:
			self.spots = np.append(self.spots, min(len(self.x)-1, self.spots[-1]+self.separation))
			num -= 1
		
	def remove(self, num):
		if len(self.spots) < num:
			self.spots = np.array([], dtype="int")
			print("ERROR in Queue visualizer remove")
		self.spots = self.spots[num:]

	def tick(self):
		d = self.data[self.counter]
		self.counter += 1
		self.add(d[1])
		self.remove(d[2])
		if len(self.spots) == 0:
			return
		if self.spots[0] >= self.walkSpeed:
			self.spots[0] -= self.walkSpeed
		elif self.spots[0] > 0:
			self.spots[0] = 0
		for i in range(1,len(self.spots)):
			if self.spots[i] > self.spots[i-1] + self.separation + self.walkSpeed:
				self.spots[i] -= self.walkSpeed
			elif self.spots[i] > self.spots[i-1] + self.separation:
				self.spots[i] = self.spots[i-1] + self.separation
		if d[0] != len(self.spots):
			print("Size error in vQueue")
				
	def getPoints(self):
		return self.x[self.spots], self.y[self.spots]