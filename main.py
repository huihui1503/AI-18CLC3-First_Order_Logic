import pygame
import numpy as np
import itertools
import sys
from pysat.solvers import Glucose3
#-----------------------data-------------------------------
class maze():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WEIGHT, HEIGHT))
        self.room=[]
        self.agent=[]
    def read_data():

class Agent():
    def __init__(self,direction,point):
        self.point=1000
        self.direction=1 #1 : north 2: south 3: East 4: west
class Room():
    def __init__(self,ID,feature):
        self.feature=feature # list of feature
        self.ID=ID
        self.discover=True

#-----------------------screen-----------------------------
HEIGHT = 750
WEIGHT = 1300
while True:
    screen.fill([192, 192, 192])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
