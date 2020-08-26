import pygame
import numpy as np
import itertools
import sys
from pysat.solvers import Glucose3
import os
import aima3.utils
import aima3.logic
#-----------------------file----------------------------
pygame.init()
filename = os.getcwd()
wall = pygame.image.load(filename + "/PICTURE/wall.png")
hero1 = pygame.image.load(filename + "/PICTURE/hero1.png")
hero2 = pygame.image.load(filename + "/PICTURE/hero2.png")
hero3 = pygame.image.load(filename + "/PICTURE/hero3.png")
hero4 = pygame.image.load(filename + "/PICTURE/hero4.png")
image_background = pygame.image.load(filename + "/PICTURE/background.jpg")
font = pygame.font.Font('freesansbold.ttf', 6)
font1 = pygame.font.Font('freesansbold.ttf', 32)
B = font.render('B', True, (0, 0, 139), (176, 224, 230))
S = font.render('S', True, (0, 0, 0), (232, 232, 232))
C = font.render('C', True, (178, 34, 34), (255, 181, 197))
G = font.render('G', True, (255, 130, 71), (255, 211, 155))
Bleeze = font1.render('B', True, (240, 128, 128))
Stench = font1.render('S', True, (240, 128, 128))
Cave = font1.render('C', True, (240, 128, 128))
Gold = font1.render('G', True, (240, 128, 128))
#-----------------------data-------------------------------


class maze():
    def __init__(self, path):
        self.screen = pygame.display.set_mode((WEIGHT, HEIGHT))
        self.room = []
        self.agent = Agent()
        self.arrow = 5
        self.size = 0
        self.clause = []
        self.read_data(path)
        # self.add_clause()

    def add_clause(self):
        self.clause.append(aima3.utils.expr(
            "Breeze(x) & Adjency(x,y) ==> Pit(y)"))

        self.clause.append(aima3.utils.expr(
            "Stench(x) & Adjency(x,y) ==> Wumpus(y)"))
        self.clause.append(aima3.utils.expr(
            "Space(x) & Adjency(x,y) ==> Safe(y)"))
        self.KB = aima3.logic.FolKB(self.clause)
        temp = self.room[10 - self.agent.position[1]
                         ][self.agent.position[0] - 1].get_adjency()
        position_agent = self.room[10 - self.agent.position[1]
                                   ][self.agent.position[0] - 1].number

    def read_data(self, path):
        file = open(path, "r")
        self.size = int(file.readline())
        for i in range(self.size):
            line = file.readline().split('.')
            temp_array = []
            for a, b in enumerate(line):
                temp = Room([a + 1, 10 - i], b)
                temp_array.append(temp)
            self.room.append(temp_array)
        # random cave
        check = True
        while check:
            x = np.random.randint(0, 9)
            y = np.random.randint(0, 9)
            if len(self.room[x][y].feature) == 0:
                self.agent.add_position([y + 1, 10 - x])
                self.room[x][y].append_feature('C')
                self.room[x][y].discover = False
                check = False
                self.agent.discover.append([y + 1, 10 - x])
                # self.clause.append(i for i in self.room[x][y].get_adjency())
        '''
        check = 5
        while check > 0:
            x = np.random.randint(0, 9)
            y = np.random.randint(0, 9)
            if not self.room[x][y].check_wumpus() and not self.room[x][y].check_pit():
                self.room[x][y].append_feature('G')
                check -= 1
        '''
        file.close()

    def test(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.room[i][j].ID)
                print(self.room[i][j].feature)

    def draw_map(self):
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
                if self.room[i][j].discover:
                    self.screen.blit(wall, (x, y))
                else:
                    if self.agent.compare_ID(self.room[i][j].ID):
                        if self.agent.direction == 1:
                            self.screen.blit(hero1, (x, y))
                        elif self.agent.direction == 2:
                            self.screen.blit(hero2, (x, y))
                        elif self.agent.direction == 3:
                            self.screen.blit(hero3, (x, y))
                        elif self.agent.direction == 4:
                            self.screen.blit(hero4, (x, y))
                        temp = 450
                        for it in self.room[i][j].feature:
                            if it == 'B':
                                self.screen.blit(Bleeze, (temp, 50))
                            elif it == 'C':
                                self.screen.blit(Cave, (temp, 50))
                            elif it == 'S':
                                self.screen.blit(Stench, (temp, 50))
                            elif it == 'G':
                                self.screen.blit(Gold, (temp, 50))
                            temp += 40
                    else:
                        temp = y
                        for it in self.room[i][j].feature:
                            if it == 'B':
                                self.screen.blit(B, (x + 3, temp))
                            elif it == 'C':
                                self.screen.blit(C, (x + 3, temp))
                            elif it == 'S':
                                self.screen.blit(S, (x + 3, temp))
                            elif it == 'G':
                                self.screen.blit(G, (x + 3, temp))
                            temp += 7
                x += 30
            y += 30

    def main_amination(self):
        mode = 1  # 1: Analysize KB, 2: find_path , 3: display movement
        list_safe = None
        list_wumpus = None
        i = 0
        path = None
        while True:
            self.draw_map()
            if mode == 1:
                list_safe, list_wumpus = self.first_order_logic()
                mode = 2
            elif mode == 2:
                if len(safe_list) == 0:
                    # calculate whether using arrow or back to cave
                    pass
                else:
                    path = self.choose_node(list_safe)
                    i = 0
            elif mode == 3:
                if i < len(path):
                    self.agent.direction = self.agent(path[i])
                    self.agent.position = path[i]
                    i += 1
                else:
                    self.agent.discover.append(self.agent.position)
                    self.room[10 - self.agent.position[1]
                              ][self.agent.position[0] - 1].discover = False
                    mode = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.update()

    def first_order_logic(self):
        current_room = self.room[10 - self.agent.position[1]
                                 ][self.agent.position[0] - 1]
        temp = current_room.get_adjency()
        position_agent = current_room.number
        if len(current_room) == 0:
            self.KB.tell(aima3.utils.expr(
                "Space(" + str(position_agent) + ")"))
        else:
            if 'S' in current_room.feature:
                self.KB.tell(aima3.utils.expr(
                    "Stench(" + str(position_agent) + ")"))
            if 'B' in current_room.feature:
                self.KB.tell(aima3.utils.expr(
                    "Breeze(" + str(position_agent) + ")"))
            if 'G' in current_room.feature:
                # pick gold
                pass
        for i in temp:
            self.KB.tell(aima3.utils.expr(
                "Adjency(" + str(position_agent) + "," + str(i) + ")"))
            self.KB.tell(aima3.utils.expr(
                "Adjency(" + str(i) + "," + str(position_agent) + ")"))
        safe = aima3.logic.fol_bc_ask(self.KB, aima3.utils.expr('Safe(y)'))
        wumpus = aima3.logic.fol_bc_ask(self.KB, aima3.utils.expr('Wumpus(x)'))
        safe_list = self.execute_safe_position(list(safe))
        wumpus_list = None
        if len(safe_list) == 0:
            wumpus_list = self.execute_wumpus_position(
                list(wumpus), list(safe))
        return safe_list, wumpus_list

    def execute_wumpus_position(self, array_wumpus, array_safe):
        wumpus = []
        for i in array_wumpus:
            check = True
            for j in array_safe:
                if i['x'] == j['y']:
                    check = False
                    break
            if check:
                wumpus.append([int(i['x'] / 10) + 1, i['x'] % 10])
        return wumpus

    def execute_safe_position(self, array):
        destination = []
        for i in array:
            if [int(i['y'] / 10) + 1, i['y'] % 10] not in self.agent.discover:
                destination.append([int(i['y'] / 10) + 1, i['y'] % 10])
        return destination

    def propositonal_logic(self):
        g = Glucose3()
        for it in self.clause:
            g.add_clause(it)
        sol = g.solve()
        if sol:
            return True, g.get_model()
        return False, None

    def choose_node(self, list_safe):
        min_cost = 9999
        path = None
        for i in list_safe:
            temp = self.BFS(i)
            if len(temp) < min_cost:
                min_cost = len(temp)
                path = temp
        return path

    def BFS(self, goal):
        return_value = []
        check_stop = True
        frontier_parent = []
        expanded_parent = []
        frontier.append(self.agent.position)
        frontier_parent.append(-1)
        while check_stop:
            if len(self.frontier) == 0:
                break
            expanded.append(frontier[0])
            frontier = frontier[1:]
            expanded_parent.append(frontier_parent[0])
            frontier_parent = frontier_parent[1:]
            self.agent.add_position([y + 1, 10 - x])
            adjacency_node = self.room[10 - frontier[1]
                                       ][frontier[0] - 1].get_adjency_position()
            for i in adjacency_node:
                if not i in expanded and i not in self.agent.discover:
                    if i[0] == goal[0] and i[1] == goal[1]:
                        expanded_parent.append(len(expanded) - 1)
                        expanded.append(i)
                        parent_pos = len(expanded) - 1
                        while parent_pos != -1:
                            return_value.append(expanded[parent_pos])
                            parent_pos = expanded_parent[parent_pos]
                        return_value = return_value[1:]
                        check_stop = False
                    else:
                        if not i in frontier:
                            frontier_parent.append(len(expanded) - 1)
                            frontier.append(i)
        return return_value


class Agent():
    def __init__(self):
        self.point = 1000
        self.direction = 1  # 1 : north 2: south 3: East 4: west
        self.position = []  # [1,1]
        self.discover = []  # [1,1] [2,2]

    def add_position(self, position):
        self.position = position

    def compare_ID(self, ID):
        return self.position[0] == ID[0] and self.position[1] == ID[1]

    def direction(self, position):
        if position[0] == self.position[0] - 1:
            return 4
        if position[0] == self.position[0] + 1:
            return 3
        if position[1] == self.position[0] - 1:
            return 2
        if position[1] == self.position[0] + 1:
            return 1


class Room():
    def __init__(self, ID, feature):
        self.feature = []  # list of feature
        self.ID = ID
        self.discover = True
        self.add_feature(feature)
        self.number = (ID[0] - 1) * 10 + ID[1]

    def add_feature(self, feature):
        for i in range(len(feature)):
            if feature[i] != '-':
                self.feature.append(feature[i])

    def check_wumpus(self):
        for i in self.feature:
            if i == 'W':
                return True
        return False

    def check_pit(self):
        for i in self.feature:
            if i == 'P':
                return True
        return False

    def append_feature(self, feature):
        self.feature.append(feature)

    def get_adjency(self):
        temp = []
        if self.ID[0] - 1 > 0:
            temp.append(self.number - 10)
        if self.ID[0] + 1 < 11:
            temp.append(self.number + 10)
        if self.ID[1] - 1 > 0:
            temp.append(self.number - 1)
        if self.ID[1] + 1 < 11:
            temp.append(self.number + 1)
        return temp

    def get_adjency_position(self):
        temp = []
        if self.ID[0] - 1 > 0:
            temp.append([ID[0] - 1, ID[1]])
        if self.ID[0] + 1 < 11:
            temp.append([ID[0] + 1, ID[1]])
        if self.ID[1] - 1 > 0:
            temp.append([ID[0] - 1, ID[1] - 1])
        if self.ID[1] + 1 < 11:
            temp.append([ID[0] - 1, ID[1] + 1])
        return temp


#-----------------------screen-----------------------------
HEIGHT = 600
WEIGHT = 1080
level_running = False
stop = True
while stop:
    maze_map = 0
    while not(level_running):
        maze_map = int(input("Enter map (1-5): "))
        if maze_map > 0 and maze_map < 6:
            level_running = True
    main = maze(filename + "/MAP/map" + str(maze_map) + ".txt")
    main.main_amination()
    # main.test()
    level_running = False
    # stop = False
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    pygame.display.update()
    '''
