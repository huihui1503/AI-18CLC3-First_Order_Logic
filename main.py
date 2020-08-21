import pygame
import numpy as np
import itertools
import sys
from pysat.solvers import Glucose3
#-----------------------file----------------------------
filename = os.getcwd()
wall = pygame.image.load(filename + "/PICTURE/wall.png")
image_hero = pygame.image.load(filename + "/PICTURE/hero.png")
image_background = pygame.image.load(filename + "/PICTURE/background1.jpg")
#-----------------------data-------------------------------


class maze():
    def __init__(self, path):
        pygame.init()
        self.screen = pygame.display.set_mode((WEIGHT, HEIGHT))
        self.room = []
        self.agent = Agent()
        self.arrow = 5
        self.size = 0
        self.read_data(path)

    def read_data(self, path):
        file = open(path, "r")
        self.size = int(file.readline())
        for i in range(self.size):
            line = file.readline().split('.')
            temp_array = []
            for a, b in enumerate(line):
                temp = Room([a + 1, 10 - i], line)
                temp_array.append(temp)
            self.room.append(temp_array)
        # random cave
        check = True
        while check:
            x = numpy.randint(0, 9)
            y = numpy.randint(0, 9)
            if not self.room[x][y].check_wumpus() and not self.room[x][y].check_pit():
                self.agent.add_position([y + 1, 10 - x])
                self.room[x][y].append_feature('C')
                check = False
        check = 5
        while check > 0:
            x = numpy.randint(0, 9)
            y = numpy.randint(0, 9)
            if not self.room[x][y].check_wumpus() and not self.room[x][y].check_pit():
                self.room[x][y].append_feature('G')
                check -= 1
        file.close()
    def draw_map():
        self.screen.fill(0)
        self.screen.blit(image_background, (0, 0))
        x = (WEIGHT - (self.size + 2) * 30) / 2
        y = (HEIGHT - (self.size + 2) * 30) / 2
        for i in range(self.size + 2):
            self.screen.blit(wall, (x + i * 30, y))
        for i in range(self.size + 2):
            self.screen.blit(wall, (x + i * 30, y + (self.size + 1) * 30))
        for i in range(self.size):
            self.screen.blit(wall, (x, y + 30 + i * 30))
        for i in range(self.size):
            self.screen.blit(wall, (x + (self.size + 1) * 30, y + 30 + i * 30))
        y += 30
        for i in range(self.size):
            x = (WEIGHT - (self.size + 2) * 30) / 2 + 30
            for j in range(self.size):
                if self.room[i][j].get_discover():
                    self.screen.blit(wall, (x, y))
                else:
                    if self.agent.compare_ID(self.room[i][j]):
                        self.screen.blit(image_hero, (x, y))
                    else:
                        pass
                        # print stench bleeze
                x += 30
            y += 30


class Agent():
    def __init__(self, direction, point):
        self.point = 1000
        self.direction = 1  # 1 : north 2: south 3: East 4: west
        self.position = []

    def add_position(self, position):
        self.position = position
    def compare_ID(self,ID):
        return self.position[0]==ID[0] and self.position[1]==ID[1]

class Room():
    def __init__(self, ID, feature):
        self.feature = []  # list of feature
        self.ID = ID
        self.discover = True
        self.add_feature(feature)

    def add_feature(self, feature):
        for i in range(len(feature)):
            if feature[i] != '-':
                self.feature.append(feature[i])

    def check_wumpus(self):
        for i in feature:
            if i == 'W':
                return True
        return False

    def check_pit(self):
        for i in feature:
            if i == 'P':
                return True
        return False

    def append_feature(self, feature):
        self.feature.append(feature)
    def get_discover(self):
        return self.discover
    def get_ID(self):
        return self.ID

#-----------------------screen-----------------------------
HEIGHT = 750
WEIGHT = 1300
while True:
    maze_map = 0
    while not(level_running):
        maze_map = int(input("Enter map (1-5): "))
        if maze_map > 0 and maze_map < 6:
            level_running = True
    main = maze(filename + "/MAP/map" + str(maze_map) + ".txt")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
