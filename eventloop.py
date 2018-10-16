import pygame
from settings import Settings
import sys

class EventLoop:
    def __init__(self, finished):
        self.finished = finished
        self.pac_moving_left = False
        self.pac_moving_right = False
        self.pac_moving_up = False
        self.pac_moving_down = False

    def __str__(self):
        return 'eventloop, finished= ' + str(self.finished) + ')'

    def check_events(self, maze):
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

    def update(self, maze, settings):
        if self.pac_moving_left == True:
            maze.pacman.rect.centerx -= settings.movement
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centerx += settings.movement

        if self.pac_moving_right == True:
            maze.pacman.rect.centerx += settings.movement
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centerx -= settings.movement

        if self.pac_moving_up == True:
            maze.pacman.rect.centery -= settings.movement
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centery += settings.movement

        if self.pac_moving_down == True:
            maze.pacman.rect.centery += settings.movement
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centery -= settings.movement
