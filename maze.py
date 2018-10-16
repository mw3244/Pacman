import pygame
from imagerect import ImageRect

class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13
    TABLET_SIZE = 7

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
        self.brick = ImageRect(screen, brickfile, self.sz, self.sz)
        self.shield = ImageRect(screen, shieldfile, self.sz, self.sz)
        self.pacman = ImageRect(screen, pacfile, self.sz * 2, self.sz * 2)
        self.clyde = ImageRect(screen, clydefile, self.sz * 2, self.sz * 2)
        self.pinky = ImageRect(screen, pinkyfile, self.sz * 2, self.sz * 2)
        self.inky = ImageRect(screen, inkyfile, self.sz * 2, self.sz * 2)
        self.blinky = ImageRect(screen, blinkyfile, self.sz * 2, self.sz * 2)
        self.powerpill = ImageRect(screen, powerfile, self.sz, self.sz)
        self.tablet = ImageRect(screen, tabletfile, self.tsz, self.tsz)
        self.deltax = self.deltay = Maze.BRICK_SIZE

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
                    self.pacman.rect = (pygame.Rect(ncol * dx, nrow * dy, self.sz * 2, self.sz * 2))
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