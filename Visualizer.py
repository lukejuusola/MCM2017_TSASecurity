import numpy as np
import matplotlib.pyplot as plt

class Visualizer:
	def __init__(self, parts, xDim, yDim, pause):
		self.parts = parts
		self.pause = pause
		
		self.x = np.array([])
		self.y = np.array([])		
		self.fig, self.ax = plt.subplots()
		self.ax.set_xlim(0, xDim) 
		self.ax.set_ylim(0, yDim)
		self.points, = self.ax.plot([], [], marker='o', linestyle='None', color='b')
		
	def tick(self, num):
		for n in range(num):
			for p in self.parts:
				p.tick()
		self.x = np.array([])
		self.y = np.array([])
		for p in self.parts:
			x, y = p.getPoints()
			self.x = np.append(self.x, x)
			self.y = np.append(self.y, y)
			
	def display(self):
		self.points.remove()
		self.points, = self.ax.plot(self.x, self.y, marker='o', linestyle='None', color='b')
		plt.pause(self.pause)
		
	def run(self, numTicks, resolution):
		for n in range(0, numTicks, resolution):
			self.tick(resolution)
			self.display()



                                
                        
