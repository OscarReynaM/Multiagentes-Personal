import agentpy as ap
import math
from Agentes.Robot import Robot

class Warehouse(ap.Model):
   
   def markTarget(self, robot: Robot):
      if not robot.getCarrying():

         if (self.robotTargetCounter == 5):
            self.robotTarget[1] = self.robotTarget[1] + 1
            robot.setTarget(self.robotTarget)
            self.robotTargetCounter = 0
            return
         else:
            robot.setTarget(self.robotTarget)
            self.robotTargetCounter += 1
            return

      minDistance = self.diagonal
      boxT = None
      boxPosT = None
      for box in self.boxes:
         if box.id in self.boxDiccionary or box.condition == 1:
            continue

         boxpos = self.grid.positions[box]
         distance = self.distanceBetweenPoints(boxpos, robot.getPosition())
         
         if distance < minDistance:
            minDistance = distance
            boxT = box
            boxPosT = boxpos

      if boxT != None:
         robot.setTarget(boxPosT)
         self.boxDiccionary[boxT.id] = robot
         
   def distanceBetweenPoints(self, point1, point2):
      return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))

   def setup(self):

      # Create space and instantiate agents
      self.grid = ap.Grid(self, [self.p.size]*2, track_empty=True)

      # Initiate Agents
      self.robots = ap.AgentList(self, self.p.robots, Robot)
      self.boxes = ap.AgentList(self, self.p["boxes"])

      # 0 for box, 1 for box moving, 2 means robot
      self.boxes.condition = 0
      self.boxes.type = "box"
      self.robots.condition = 2
      # 3 el stack tiene una caja, 4 stack tiene 2 cajas, 5 stack tiene 3 cajas, 6 stack tiene 4 cajas, 7 stack tiene 5 cajas 

      # Add agents to the grid
      self.grid.add_agents(self.boxes, random=True, empty=True)
      self.grid.add_agents(self.robots, random=True, empty=True)
      

      print("Cantidad de Robots: ", self.p.robots)
      print("Cantidad de Cajas: ", self.p["boxes"])

      #Sets up position to have the grid of the robot on the grid
      self.robots.setupPosition(self.grid)
      self.robotTarget = [0, 0]
      self.robotTargetCounter = 0

      # Calculate diagonal
      self.diagonal = int(math.sqrt(math.pow(self.p.size, 2)))
      self.robots.setDiagonal(self.diagonal)

      # Diccionary for the bots to dont fight for the boxes
      self.boxDiccionary = {}

      for robot in self.robots:
         robot.setCarrying(True)
         self.markTarget(robot)

      
   def step(self):
      for robot in self.robots:
         robot.step()
         if (robot.getCarrying()):
            distance = self.distanceBetweenPoints(robot.getPosition(), robot.getTargetPosition())
            if abs(distance) <= 1:
               box = self.grid.agents[robot.getTargetPosition()].to_list()
               for agent in box:
                  if agent.type == "box":
                     box = agent
               box.condition = 1
               robot.incrementalCounter()
               self.markTarget(robot)
         else:
            robotGoal = abs(self.distanceBetweenPoints(robot.getPosition(), self.goal))
            print("")
            if (robotGoal <= 1):
               self.goal = [self.goal[0]+1, self.goal[1]+1]



               robot.setCarrying(True)
               self.markTarget(robot)


               
               
      







      