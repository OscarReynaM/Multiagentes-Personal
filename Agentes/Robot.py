import agentpy as ap
from agentpy import model
import numpy as np

class Robot(ap.Agent):

   def setup(self):
      self.target = (0, 0)
      self.carrying = False
      self.boxCount = 0

   def setupPosition(self, grid):
      self.grid = grid
      self.position = grid.positions[self]

   def getPosition(self):
      return self.position

   def setDiagonal(self, diag):
      self.diagonal = diag

   def getCarrying(self):
      return self.carrying

   def setCarrying(self, conditional):
      self.carrying = conditional

   def getTargetPosition(self):
      return self.target

   def incrementalCounter(self):
      self.boxCount += 1
      if (self.boxCount == 2):
         self.carrying = False
         self.boxCount = 0

   def getVector(self): #Creates vector to be used in the move_by for the grid
      deltaY = self.target[0] - self.position[0]
      deltaX = self.target[1] - self.position[1]

      if deltaX == 0 and deltaY == 0:
         return (0, 0)

      vector = np.array([deltaY, deltaX])
      vector = vector / np.linalg.norm(vector)
      vector = vector.tolist()
      vector[0] = int(round(vector[0]))
      vector[1] = int(round(vector[1]))

      return vector

   def setTarget(self, target : tuple):
      self.target = target
      self.carrying = True
      self.vector = self.getVector()


   

   



   

