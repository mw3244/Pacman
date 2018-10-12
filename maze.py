import pygame
from imagerect import ImageRect

class Maze:
    RED = (255, 0, 0)
    BRICK_SIZE = 13

    def __init__(self, screen, mazefile, brickfile, shieldfile, pacfile, powerfile):
        self.screen = screen
        self.filename = mazefile
        with open(self.filename, 'r') as f:
            self.rows = f.readlines()

        self.shields = []
        self.bricks = []
        self.powerpills = []
        sz = Maze.BRICK_SIZE
        self.brick = ImageRect(screen, brickfile, sz, sz)
        self.shield = ImageRect(screen, shieldfile, sz, sz)
        self.pacman = ImageRect(screen, pacfile, sz * 2, sz * 2)
        self.powerpill = ImageRect(screen, powerfile, sz, sz)
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
                    self.pacman.rect = (pygame.Rect(ncol * dx, nrow * dy, w, h))
                if col == 'p':
                    self.powerpills.append(pygame.Rect(ncol * dx, nrow * dy, w, h))

    def blitme(self):
        for rect in self.bricks:
            self.screen.blit(self.brick.image, rect)
        for rect in self.shields:
            self.screen.blit(self.shield.image, rect)
        self.screen.blit(self.pacman.image,self.pacman.rect)
        for rect in self.powerpills:
            self.screen.blit(self.powerpill.image, rect)