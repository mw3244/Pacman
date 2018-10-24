import pygame
from imagerect import ImageRect
from dijkstra import Dijkstra

class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13
    TABLET_SIZE = 7
    PAC_SIZE = 39

    def __init__(self, screen, mazefile, brickfile, shieldfile, pacfile, powerfile, tabletfile, clydefile, pinkyfile,
                 inkyfile, blinkyfile):
        self.screen = screen
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.shields = []
        self.bricks = []
        self.powerpills = []
        self.tablets = []
        self.sz = Maze.BRICK_SIZE
        self.tsz = Maze.TABLET_SIZE
        self.psz = Maze.PAC_SIZE
        self.brick = ImageRect(screen, brickfile, self.sz, self.sz)
        self.shield = ImageRect(screen, shieldfile, self.sz, self.sz)
        self.pacman = ImageRect(screen, pacfile, self.psz, self.psz)
        self.clyde = ImageRect(screen, clydefile, self.sz * 2, self.sz * 2)
        self.pinky = ImageRect(screen, pinkyfile, self.sz * 2, self.sz * 2)
        self.inky = ImageRect(screen, inkyfile, self.sz * 2, self.sz * 2)
        self.blinky = ImageRect(screen, blinkyfile, self.sz * 2, self.sz * 2)
        self.powerpill = ImageRect(screen, powerfile, self.sz, self.sz)
        self.tablet = ImageRect(screen, tabletfile, self.tsz, self.tsz)

        self.deltax = self.deltay = Maze.BRICK_SIZE
        self.nodeDict = {}
        self.currentnodeDict = {}
        self.nodeXYDict = {}
        self.XYnodeDict = {}

        self.build()

    def __str__(self): return 'maze(' + self.filename + ')'

    def build(self):
        r = self.brick.rect
        w, h = r.width, r.height
        dx, dy = self.deltax, self.deltay

        for nrow in range(len(self.rows)):
            row = self.rows[nrow]
            for ncol in range(len(row)):
                col = row [ncol]
                if col == 'x':
                    self.bricks.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 's':
                    self.shields.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'P':
                    self.pacman.rect = (pygame.Rect(ncol * dx, nrow * dy, self.psz, self.psz))
                if col == 'p':
                    self.powerpills.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 't':
                    self.tablets.append(pygame.Rect(ncol * dx, nrow * dy, self.tsz, self.tsz))
                if col == 'c':
                    self.clyde.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                if col == 'n':
                    self.pinky.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                if col == 'i':
                    self.inky.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                if col == 'b':
                    self.blinky.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                if col != 'x' and col != 'q' and col != '\n':
                    if self.eightwaycheck(nrow, ncol):
                        self.nodeXYDict[str(str(nrow) + str(ncol))] = ncol * dx, nrow * dy
                        self.XYnodeDict[str(str(ncol * dx)+ ' ' + str(nrow * dy))] = str(str(nrow) + str(ncol))
                        if self.eightwaycheck(nrow, ncol - 1):
                            self.currentnodeDict[str(str(nrow) + str(ncol - 1))] = 1
                        if self.eightwaycheck(nrow, ncol + 1):
                            self.currentnodeDict[str(str(nrow) + str(ncol + 1))] = 1
                        if self.eightwaycheck(nrow + 1, ncol):
                            self.currentnodeDict[str(str(nrow + 1) + str(ncol))] = 1
                        if self.eightwaycheck(nrow - 1, ncol):
                            self.currentnodeDict[str(str(nrow - 1) + str(ncol))] = 1
                        self.nodeDict[str(str(nrow) + str(ncol))] = self.currentnodeDict
                        self.currentnodeDict = {}
        #print(self.nodeXYDict['82'])
        #XY = self.nodeXYDict['82']
        #print(XY[0])
        #print(self.XYnodeDict)
        #Dijkstra('2921', '4421', self.nodeDict)

    def eightwaycheck (self, nrow, ncol):
        if self.rows[nrow - 1][ncol - 1] == 'x':
            return False
        if self.rows[nrow][ncol - 1] == 'x':
            return False
        if self.rows[nrow + 1][ncol - 1] == 'x':
            return False
        if self.rows[nrow - 1][ncol] == 'x':
            return False
        if self.rows[nrow + 1][ncol] == 'x':
            return False
        if self.rows[nrow - 1][ncol + 1] == 'x':
            return False
        if self.rows[nrow][ncol + 1] == 'x':
            return False
        if self.rows[nrow + 1][ncol + 1] == 'x':
            return False
        return True

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.shields:
            self.screen.blit(self.shield.image, rect)
        for rect in self.powerpills:
            self.screen.blit(self.powerpill.image, rect)
        for rect in self.tablets:
            self.screen.blit(self.tablet.image, rect)
        self.screen.blit(self.pacman.image, self.pacman.rect)
        self.screen.blit(self.clyde.image, self.clyde.rect)
        self.screen.blit(self.pinky.image, self.pinky.rect)
        self.screen.blit(self.inky.image, self.inky.rect)
        self.screen.blit(self.blinky.image, self.blinky.rect)