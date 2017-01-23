import numpy as np
import csv
from functions import makeData

class vHolder:
	def __init__(self, xRange, yRange, orientation, file):
		self.xRange = xRange
		self.yRange = yRange
		
		self.data = []
		file = open(file, 'r')
		r = csv.reader(file, delimiter=",")
		for row in r:
			row = np.array(row).astype(int)
			self.data.append(row)
		self.holder = np.array([])
		self.counter = 0
		
		if orientation:
			self.dist = yRange[-1]-yRange[0]
		else:
			self.dist = xRange[-1]-xRange[0]
		self.orientation = orientation
		
		self.x = np.array([])
		self.y = np.array([])
		self.speeds = np.array([])
		
	def add(self, waits):
		self.holder = np.append(self.holder, waits)
		if self.orientation:
			for n in range(len(waits)):
				self.x = np.append(self.x, np.random.choice(self.xRange))
				self.y = np.append(self.y, np.array(self.yRange[0]))
		else:
			for n in range(len(waits)):
				self.y = np.append(self.y, np.random.choice(self.yRange))
				self.x = np.append(self.x, np.array(self.xRange[0]))
		self.speeds = np.append(self.speeds, self.dist/np.array(waits))
		
				
	def remove(self):
		idx = np.where(self.holder <= 0)[0][:self.data[self.counter][1]]
		self.holder = np.delete(self.holder, idx)
		self.x = np.delete(self.x, idx)
		self.y = np.delete(self.y, idx)
		self.speeds = np.delete(self.speeds, idx)

	def tick(self):
	
		self.holder -= 1
		
		if self.orientation:
			self.y += self.speeds
			self.y[self.y > self.yRange[-1]] = self.yRange[-1]
		else:
			self.x += self.speeds
			self.x[self.x > self.xRange[-1]] = self.xRange[-1]
		
		if len(self.data[self.counter]) > 2:
			self.add(self.data[self.counter][2:])
		self.remove()
			
#		if self.data[self.counter][0] != len(self.x):
#			print("Size error in vHolder x")
#		if self.data[self.counter][0] != len(self.y):
#			print("Size error in vHolder y")
#		if self.data[self.counter][0] != len(self.holder):
#			print("Size error in vHolder holder")
#		if self.data[self.counter][0] != len(self.speeds):
#			print("Size error in vHolder speeds")
			
		self.counter += 1
				
	def getPoints(self):
		return self.x, self.y