import pygame
from settings import Settings
import sys
from imagerect import ImageRect
from dijkstra import Dijkstra
import math

class EventLoop:
    def __init__(self, maze, finished):
        self.settings = Settings()
        self.maze = maze
        self.finished = finished
        self.pac_moving_left = False
        self.pac_moving_right = False
        self.pac_moving_up = False
        self.pac_moving_down = False
        self.pac_left_animation = 'images/left_bigman_1.png'
        self.pac_right_animation = 'images/right_bigman_1.png'
        self.pac_up_animation = 'images/up_bigman_1.png'
        self.pac_down_animation = 'images/down_bigman_1.png'
        self.pac_animation_clock = self.settings.pac_animation_clock
        self.search_clock = self.settings.search_clock
        self.clyde_path = []
        self.pinky_path = []
        self.inky_path = []
        self.blinky_path = []
        self.ghost_move_OK = False

    def __str__(self):
        return 'eventloop, finished= ' + str(self.finished) + ')'

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pac_moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.pac_moving_right = True
                if event.key == pygame.K_UP:
                    self.pac_moving_up = True
                if event.key == pygame.K_DOWN:
                    self.pac_moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.pac_moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.pac_moving_right = False
                if event.key == pygame.K_UP:
                    self.pac_moving_up = False
                if event.key == pygame.K_DOWN:
                    self.pac_moving_down = False

    def update(self, settings, screen):
        if self.pac_moving_left == True:
            self.maze.pacman.rect.centerx -= settings.movement
            img = pygame.image.load(self.pac_left_animation)
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
        if self.maze.pacman.rect.collidelist(self.maze.bricks) >= 0 or self.maze.pacman.rect.collidelist(self.maze.shields) >= 0:
            self.maze.pacman.rect.centerx += settings.movement

        if self.pac_moving_right == True:
            self.maze.pacman.rect.centerx += settings.movement
            img = pygame.image.load(self.pac_right_animation)
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
        if self.maze.pacman.rect.collidelist(self.maze.bricks) >= 0 or self.maze.pacman.rect.collidelist(self.maze.shields) >= 0:
            self.maze.pacman.rect.centerx -= settings.movement

        if self.pac_moving_up == True:
            self.maze.pacman.rect.centery -= settings.movement
            img = pygame.image.load(self.pac_up_animation)
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
        if self.maze.pacman.rect.collidelist(self.maze.bricks) >= 0 or self.maze.pacman.rect.collidelist(self.maze.shields) >= 0:
            self.maze.pacman.rect.centery += settings.movement

        if self.pac_moving_down == True:
            self.maze.pacman.rect.centery += settings.movement
            img = pygame.image.load(self.pac_down_animation)
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
        if self.maze.pacman.rect.collidelist(self.maze.bricks) >= 0 or self.maze.pacman.rect.collidelist(self.maze.shields) >= 0:
            self.maze.pacman.rect.centery -= settings.movement

        tablet_collision = self.maze.pacman.rect.collidelist(self.maze.tablets)
        if tablet_collision >= 0:
            del self.maze.tablets[tablet_collision]

        self.pac_animation_clock -= 1

        cascade_stop = False
        if self.pac_animation_clock <= 0:
            if self.pac_left_animation == 'images/bigman_3.png':
                self.pac_left_animation = 'images/left_bigman_1.png'
                self.pac_right_animation = 'images/right_bigman_1.png'
                self.pac_up_animation = 'images/up_bigman_1.png'
                self.pac_down_animation = 'images/down_bigman_1.png'
                cascade_stop = True

            if self.pac_left_animation == 'images/left_bigman_2.png':
                self.pac_left_animation = 'images/bigman_3.png'
                self.pac_right_animation = 'images/bigman_3.png'
                self.pac_up_animation = 'images/bigman_3.png'
                self.pac_down_animation = 'images/bigman_3.png'

            if self.pac_left_animation == 'images/left_bigman_1.png' and cascade_stop == False:
                self.pac_left_animation = 'images/left_bigman_2.png'
                self.pac_right_animation = 'images/right_bigman_2.png'
                self.pac_up_animation = 'images/up_bigman_2.png'
                self.pac_down_animation = 'images/down_bigman_2.png'

            self.pac_animation_clock = self.settings.pac_animation_clock

        self.search_clock -= 1

        if self.search_clock == 150:
            pacNode = self.getObjectNode("pacman")
            clydeNode = self.getObjectNode("clyde")
            self.clyde_path = Dijkstra(clydeNode, pacNode, self.maze.nodeDict)
        if self.search_clock == 100:
            pacNode = self.getObjectNode("pacman")
            pinkyNode = self.getObjectNode("pinky")
            self.pinky_path = Dijkstra(pinkyNode, pacNode, self.maze.nodeDict)
        if self.search_clock == 50:
            pacNode = self.getObjectNode("pacman")
            inkyNode = self.getObjectNode("inky")
            self.inky_path = Dijkstra(inkyNode, pacNode, self.maze.nodeDict)
        if self.search_clock <= 0:
            pacNode = self.getObjectNode("pacman")
            blinkyNode = self.getObjectNode("blinky")
            self.blinky_path = Dijkstra(blinkyNode, pacNode, self.maze.nodeDict)
            self.search_clock = self.settings.search_clock

        self.updateGhost("clyde")
        self.updateGhost("pinky")
        self.updateGhost("inky")
        self.updateGhost("blinky")

    def updateGhost(self, identifier):
        if identifier == "clyde":
            path = self.clyde_path
            xObj = self.maze.clyde.rect.centerx
            yObj = self.maze.clyde.rect.centery
        elif identifier == "pinky":
            path = self.pinky_path
            xObj = self.maze.pinky.rect.centerx
            yObj = self.maze.pinky.rect.centery
        elif identifier == "inky":
            path = self.inky_path
            xObj = self.maze.inky.rect.centerx
            yObj = self.maze.inky.rect.centery
        elif identifier == "blinky":
            path = self.blinky_path
            xObj = self.maze.blinky.rect.centerx
            yObj = self.maze.blinky.rect.centery
        else:
            path = None
            xObj = None
            yObj = None

        if path:
            XY = self.maze.nodeXYDict[path[0]]
            XDest = XY[0]
            YDest = XY[1]

            if XDest == xObj and YDest == yObj:
                del path[0]
            if XDest > xObj:
                xObj+= self.settings.ghost_movement
            elif XDest < xObj:
                xObj-= self.settings.ghost_movement
            if YDest > yObj:
                yObj+= self.settings.ghost_movement
            elif YDest < yObj:
                yObj-= self.settings.ghost_movement

            if identifier == "clyde":
                self.maze.clyde.rect.centerx = xObj
                self.maze.clyde.rect.centery = yObj
                self.clyde_path = path
            elif identifier == "pinky":
                self.maze.pinky.rect.centerx = xObj
                self.maze.pinky.rect.centery = yObj
                self.pinky_path = path
            elif identifier == "inky":
                self.maze.inky.rect.centerx = xObj
                self.maze.inky.rect.centery = yObj
                self.inky_path = path
            elif identifier == "blinky":
                self.maze.blinky.rect.centerx = xObj
                self.maze.blinky.rect.centery = yObj
                self.blinky_path = path

    def getObjectNode(self, identifier):
        if identifier == "clyde":
            xObj = self.maze.clyde.rect.centerx
            yObj = self.maze.clyde.rect.centery
        elif identifier == "pinky":
            xObj = self.maze.pinky.rect.centerx
            yObj = self.maze.pinky.rect.centery
        elif identifier == "inky":
            xObj = self.maze.inky.rect.centerx
            yObj = self.maze.inky.rect.centery
        elif identifier == "blinky":
            xObj = self.maze.blinky.rect.centerx
            yObj = self.maze.blinky.rect.centery
        elif identifier == "pacman":
            xObj = self.maze.pacman.rect.centerx
            yObj = self.maze.pacman.rect.centery
        else:
            xObj = None
            yObj = None
        nodeXYDict = self.maze.nodeXYDict
        XYnodeDict = self.maze.XYnodeDict
        bestFitNode = None
        bestFitDistance = 9999

        for i in nodeXYDict:
            node = nodeXYDict[i]
            xNode = node[0]
            yNode = node[1]

            testDistance = math.sqrt(((xObj - xNode)**2) + ((yObj - yNode)**2))
            if testDistance < bestFitDistance:
                bestFitDistance = testDistance
                bestFitNode = XYnodeDict[str(xNode) + ' ' + str(yNode)]
        return bestFitNode
