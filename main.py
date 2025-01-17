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
clock = pygame.time.Clock()
wall = pygame.image.load(filename + "/PICTURE/wall.png")
hero1 = pygame.image.load(filename + "/PICTURE/hero1.png")
hero2 = pygame.image.load(filename + "/PICTURE/hero2.png")
hero3 = pygame.image.load(filename + "/PICTURE/hero3.png")
hero4 = pygame.image.load(filename + "/PICTURE/hero4.png")
image_background = pygame.image.load(filename + "/PICTURE/background.jpg")
font = pygame.font.Font('freesansbold.ttf', 10)
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
        self.size = 0
        self.cave = None
        self.clause = []
        self.read_data(path)
        # self.test()
        self.add_clause()

    def add_clause(self):
        self.clause.append(aima3.utils.expr(
            "Breeze(x) & Adjency(x,y) ==> Pit(y)"))

        self.clause.append(aima3.utils.expr(
            "Stench(x) & Adjency(x,y) ==> Wumpus(y)"))
        self.clause.append(aima3.utils.expr(
            "Space(x) & Adjency(x,y) ==> Safe(y)"))
        self.agent.KB = aima3.logic.FolKB(self.clause)

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
                self.cave = [y + 1, 10 - x]
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
                print(self.room[i][j].ID, end=' ')
                print(self.room[i][j].feature, end=' ')
                print(len(self.room[i][j].feature))

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
                        surf = None
                        if self.agent.direction == 1:
                            surf = pygame.transform.rotate(hero1, 0)
                        elif self.agent.direction == 2:
                            surf = pygame.transform.rotate(hero1, 180)
                        elif self.agent.direction == 3:
                            surf = pygame.transform.rotate(hero1, 90)
                        else:
                            surf = pygame.transform.rotate(hero1, -90)
                        self.screen.blit(surf, (x, y))
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
                            temp += 10
                x += 30
            y += 30

    def main_animation(self):
        mode = 1  # 1: Analysize KB and take action, 2: Do action in code , 3: display action in graphic
        list_safe = []
        list_wumpus = None
        list_pit = None
        i = 0
        path = None
        goal = None
        check_stop = True
        # self.draw_map()
        while check_stop:
            clock.tick(10)
            if mode == 1:
                list_safe, list_wumpus, list_pit = self.agent.first_order_logic(
                    self.room)
                goal, path, action = self.agent.take_action(
                    list_safe, list_wumpus, list_pit, self.room, self.cave)
                i = 0
                mode = 2
            elif mode == 2:
                if i < len(path):
                    self.agent.set_direction(self.agent.get_direction(path[i]))
                    self.agent.position = path[i]
                    self.agent.point -= 10
                    i += 1
                else:
                    if action == 21:  # Go to safe
                        self.agent.discover.append(goal)
                        self.room[10 - goal[1]][goal[0] - 1].discover = False
                    elif action == 22:  # Shoot
                        self.agent.set_direction(
                            self.agent.get_direction(goal))  # Face to wumpus
                        self.agent.shoot_arrow(goal, list_pit)
                        self.agent.point -= 100
                        self.remove_wumpus(goal)
                    mode = 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.draw_map()
            print("Point: " + str(self.agent.point))
            if mode != 2:
                check_stop = self.terminal(list_safe)
            pygame.display.update()
            
    def remove_wumpus(self, wumpus):
        wumpus_room = self.room[10 - wumpus[1]][wumpus[0] - 1]
        if 'W' in wumpus_room.feature:  # If has wumpus => remove
            wumpus_room.feature.pop(wumpus_room.feature.index('W'))
            adjency_wumpus_room = wumpus_room.get_adjency_position()

            for a1 in adjency_wumpus_room:
                pos_room = self.room[10 - a1[1]][a1[0] - 1]
                adjency_room = pos_room.get_adjency_position()
                check = False
                for a2 in adjency_room:
                    if 'W' in self.room[10 - a2[1]][a2[0] - 1].feature:
                        check = True
                        break
                if check == False:
                    pos_room.feature.pop(pos_room.feature.index('S'))
                    if pos_room.discover and len(pos_room.feature) == 0:
                        self.agent.KB.tell(aima3.utils.expr(
                            "Space(" + str(pos_room.number) + ")"))
    def terminal(self, list_safe):
        current_room = self.room[10 - self.agent.position[1]
                                 ][self.agent.position[0] - 1]
        if 'P' in current_room.feature:
            print('P')
            print(self.agent.position)
            self.agent.point = self.agent.point - 10000
            return False
        if 'W' in current_room.feature:
            print('W')
            print(self.agent.position)
            self.agent.point = self.agent.point - 10000
            return False
        if len(list_safe) == 1 and self.cave in list_safe:
            print('C')
            self.agent.point = self.agent.point + 10
            return False
        return True


class Agent():
    def __init__(self):
        self.arrow = 3
        self.point = 1000
        self.direction = 1  # 1 : north 2: south 3: East 4: west
        self.position = []  # [1,1]
        self.discover = []  # [1,1] [2,2]
        self.KB = None

    def add_position(self, position):
        self.position = position

    def compare_ID(self, ID):
        return self.position[0] == ID[0] and self.position[1] == ID[1]

    def get_direction(self, position):
        if position[0] - 1 == self.position[0]:
            return 4
        if position[0] + 1 == self.position[0]:
            return 3
        if position[1] - 1 == self.position[0]:
            return 2
        if position[1] + 1 == self.position[0]:
            return 1

    def set_direction(self, direction):
        self.direction = direction

    def take_action(self, list_safe, list_wumpus, list_pit, room, cave):
        print("Action:", end=" ")
        mode = 21
        path = []
        goal = []
        if len(list_safe) == 0:
            if 100 - (len(list_wumpus) + len(list_pit) + len(list_safe)) <= 10:
                print("back to cave", end=" ")
                list_safe.append(cave)
            else:
                temp = []
                for i in list_wumpus:
                    if i not in list_pit:
                        temp.append(i)
                path, goal = self.choose_node(temp, room)
                if len(path) == 0:
                    print("back to cave", end=" ")
                    list_safe.append(cave)
                else:
                    print("use arrow to room: " + str(goal))
                    path = path[:len(path) - 1]
                    mode = 22
        if mode == 21:
            path, goal = self.choose_node(list_safe, room)
            print("find way to room: " + str(goal))
        return goal, path, mode

    def shoot_arrow(self, wumpus, pit):
        room_wumpus = (wumpus[0] - 1) * 10 + wumpus[1]
        if wumpus not in pit:
            print('wumpus -> safe: ' + str(wumpus))
            self.KB.tell(aima3.utils.expr("Safe(" + str(room_wumpus) + ")"))

    def first_order_logic(self, room):
        print("New knowledge of each room:", end=" ")
        current_room = room[10 - self.position[1]
                            ][self.position[0] - 1]
        temp = current_room.get_adjency_position()
        position_agent = current_room.number
        if len(current_room.feature) == 0 or 'C' in current_room.feature:
            self.KB.tell(aima3.utils.expr(
                "Space(" + str(position_agent) + ")"))
            print("Space(" + str(position_agent) + ")", end=" ")
        else:
            i = 0
            while i < len(current_room.feature):
                if current_room.feature[i] == 'S':
                    self.KB.tell(aima3.utils.expr(
                        "Stench(" + str(position_agent) + ")"))
                    print("Stench(" + str(position_agent) + ")", end=" ")
                if current_room.feature[i] == 'B':
                    self.KB.tell(aima3.utils.expr(
                        "Breeze(" + str(position_agent) + ")"))
                    print("Breeze(" + str(position_agent) + ")", end=" ")
                if current_room.feature[i] == 'G':
                    self.point += 100
                    if len(current_room.feature) == 1:
                        self.KB.tell(aima3.utils.expr(
                            "Space(" + str(position_agent) + ")"))
                        print("Space(" + str(position_agent) + ")", end=" ")
                    current_room.feature.pop(
                        current_room.feature.index('G'))
                    print("Gold(" + str(position_agent) + ")", end=" ")
                    i -= 1
                i += 1
        for i in temp:
            if i not in self.discover:
                self.KB.tell(aima3.utils.expr(
                    "Adjency(" + str(position_agent) + "," + str((i[0] - 1) * 10 + i[1]) + ")"))
                print("Adjency(" + str(position_agent) + "," +
                      str((i[0] - 1) * 10 + i[1]) + ")", end=" ")
                self.KB.tell(aima3.utils.expr(
                    "Adjency(" + str((i[0] - 1) * 10 + i[1]) + "," + str(position_agent) + ")"))
                print("Adjency(" + str((i[0] - 1) * 10 + i[1]) +
                      "," + str(position_agent) + ")", end=" ")
        safe = list(aima3.logic.fol_bc_ask(
            self.KB, aima3.utils.expr('Safe(y)')))
        wumpus = list(aima3.logic.fol_bc_ask(
            self.KB, aima3.utils.expr('Wumpus(x)')))
        pit = list(aima3.logic.fol_bc_ask(
            self.KB, aima3.utils.expr('Pit(x)')))
        safe_list = self.execute_safe_position(safe)
        wumpus_list = None
        pit_list = None
        wumpus_list = self.execute_wumpus_position(wumpus, safe)
        pit_list = self.execute_pit_position(pit, safe)
        print("")
        print("List of wumpus: " + str(wumpus_list))
        print("List of pit: " + str(pit_list))
        print("List of safe: " + str(safe_list))
        return safe_list, wumpus_list, pit_list

    def execute_pit_position(self, array_pit, array_safe):
        pit = []
        for i in array_pit:
            check = True
            for j in array_safe:
                if i[aima3.utils.expr('x')] == j[aima3.utils.expr('y')]:
                    check = False
                    break
            if check:
                if i[aima3.utils.expr('x')] % 10 == 0:
                    value = [int(i[aima3.utils.expr('x')] / 10), 10]
                else:
                    value = [int(i[aima3.utils.expr('x')] / 10) +
                             1, i[aima3.utils.expr('x')] % 10]
                if value not in pit:
                    pit.append(value)
        return pit

    def execute_wumpus_position(self, array_wumpus, array_safe):
        wumpus = []
        for i in array_wumpus:
            check = True
            for j in array_safe:
                if i[aima3.utils.expr('x')] == j[aima3.utils.expr('y')]:
                    check = False
                    break
            if check:
                if i[aima3.utils.expr('x')] % 10 == 0:
                    value = [int(i[aima3.utils.expr('x')] / 10), 10]
                else:
                    value = [int(i[aima3.utils.expr('x')] / 10) +
                             1, i[aima3.utils.expr('x')] % 10]
                if value not in wumpus:
                    wumpus.append(value)
        return wumpus

    def execute_safe_position(self, array):
        destination = []
        for i in array:
            value = i[aima3.utils.expr('y')]
            compare_value = None
            if value % 10 == 0:
                compare_value = [int(value / 10), 10]
            else:
                compare_value = [int(value / 10) + 1, value % 10]
            if compare_value not in self.discover and compare_value not in destination:
                # print([int(value / 10) + 1, value % 10])
                destination.append(compare_value)
        return destination

    def choose_node(self, list_safe, room):
        min_cost = 9999
        path = []
        goal = []
        for i in list_safe:
            temp = self.BFS(i, room)
            if len(temp) < min_cost and len(temp) != 0:
                min_cost = len(temp)
                path = temp
                goal = i
        return path, goal

    def BFS(self, goal, room):
        return_value = []
        check_stop = True
        frontier_parent = []
        expanded_parent = []
        frontier = []
        expanded = []
        frontier.append(
            (self.position[0] - 1) * 10 + self.position[1])
        frontier_parent.append(-1)
        while check_stop:
            if len(frontier) == 0:
                break
            expanded.append(frontier[0])
            expanded_parent.append(frontier_parent[0])
            if frontier[0] % 10 == 0:
                adjacency_node = room[0][int(
                    frontier[0] / 10) - 1].get_adjency()
            else:
                adjacency_node = room[10 - (frontier[0] % 10)
                                      ][int(frontier[0] / 10)].get_adjency()
            frontier_parent = frontier_parent[1:]
            frontier = frontier[1:]

            for i in adjacency_node:
                if not i in expanded:
                    temp_value = None
                    if i % 10 == 0:
                        temp_value = [int(i / 10), 10]
                    else:
                        temp_value = [int(i / 10) + 1, i % 10]
                    if i == ((goal[0] - 1) * 10 + goal[1]):
                        expanded_parent.append(len(expanded) - 1)
                        expanded.append(i)
                        parent_pos = len(expanded) - 1
                        while parent_pos != -1:
                            return_value.append(expanded[parent_pos])
                            parent_pos = expanded_parent[parent_pos]
                        return_value = return_value[:: -1]
                        return_value = return_value[1:]
                        check_stop = False
                    elif temp_value in self.discover:
                        if not i in frontier:
                            frontier_parent.append(len(expanded) - 1)
                            frontier.append(i)
        path = []
        for i in return_value:
            if i % 10 == 0:
                path.append([int(i / 10), 10])
            else:
                path.append([int(i / 10) + 1, i % 10])
        return path


class Room():
    def __init__(self, ID, feature):
        self.feature = []  # list of feature
        self.ID = ID
        self.discover = True
        self.add_feature(feature)
        self.number = (ID[0] - 1) * 10 + ID[1]

    def add_feature(self, feature):
        for i in range(len(feature)):
            if feature[i] != '-' and feature[i] != '\n':
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
            temp.append([self.ID[0] - 1, self.ID[1]])
        if self.ID[0] + 1 < 11:
            temp.append([self.ID[0] + 1, self.ID[1]])
        if self.ID[1] - 1 > 0:
            temp.append([self.ID[0], self.ID[1] - 1])
        if self.ID[1] + 1 < 11:
            temp.append([self.ID[0], self.ID[1] + 1])
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
        if maze_map == -1:
            level_running = True
            stop = False
    if stop:
        main = maze(filename + "/MAP/map" + str(maze_map) + ".txt")
        main.main_animation()
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
