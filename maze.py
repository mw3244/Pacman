import pygame
from imagerect import ImageRect
from dijkstra import Dijkstra
from button import Text
from button import Picture
from stats import Stats


class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13
    TABLET_SIZE = 7
    PAC_SIZE = 39

    def __init__(self, screen, mazefile, brickfile, shieldfile, pacfile, powerfile, tabletfile, clydefile, pinkyfile,
                 inkyfile, blinkyfile, stats):
        self.screen = screen
        self.filename = mazefile
        self.stats = stats
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()


        self.score_text = Text(self.screen, "SCORE:", 50, 50, 20, 20, (255, 255, 255))
        self.lives_text = Text(self.screen, "LIVES:", 50, 50, 300, 20, (255, 255, 255))

        self.shields = []
        self.bricks = []
        self.powerpills = []
        self.tablets = []
        self.life = [None] * 5
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
        self.life_image = pygame.image.load('images/left_pac_1.png')

        self.deltax = self.deltay = Maze.BRICK_SIZE
        self.nodeDict = {}
        self.currentnodeDict = {}
        self.nodeXYDict = {}
        self.XYnodeDict = {}

        self.pacman_init_x = 0
        self.pacman_init_y = 0
        self.clyde_init_x = 0
        self.clyde_init_y = 0
        self.pinky_init_x = 0
        self.pinky_init_y = 0
        self.inky_init_x = 0
        self.inky_init_y = 0
        self.blinky_init_x = 0
        self.blinky_init_y = 0

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
                    self.pacman_init_x = ncol * dx
                    self.pacman_init_y = nrow * dy
                if col == 'p':
                    self.powerpills.append(pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 't':
                    self.tablets.append(pygame.Rect(ncol * dx, nrow * dy, self.tsz, self.tsz))
                if col == 'c':
                    self.clyde.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                    self.clyde_init_x = ncol * dx
                    self.clyde_init_y = nrow * dy
                if col == 'n':
                    self.pinky.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                    self.pinky_init_x = ncol * dx
                    self.pinky_init_y = nrow * dy
                if col == 'i':
                    self.inky.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                    self.inky_init_x = ncol * dx
                    self.inky_init_y = nrow * dy
                if col == 'b':
                    self.blinky.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
                    self.blinky_init_x = ncol * dx
                    self.blinky_init_y = nrow * dy
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
        self.score_text.draw_text()
        self.score = Text(self.screen, str(self.stats.score), 50, 50, 155, 20, (255, 255, 255))
        self.score.draw_text()
        self.lives_text.draw_text()
        for i in range (self.stats.lives):
            if i <= 4:
                self.life[i] = Picture(self.screen, 420 + (i * 30), 20, self.life_image)
                self.life[i].draw_picture()