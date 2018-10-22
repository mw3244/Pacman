import pygame
from settings import Settings
import sys
from imagerect import ImageRect

class EventLoop:
    def __init__(self, finished):
        self.settings = Settings()
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

    def update(self, maze, settings, screen):
        if self.pac_moving_left == True:
            maze.pacman.rect.centerx -= settings.movement
            img = pygame.image.load(self.pac_left_animation)
            img = pygame.transform.scale(img, (maze.psz, maze.psz))
            maze.pacman.image = img
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centerx += settings.movement

        if self.pac_moving_right == True:
            maze.pacman.rect.centerx += settings.movement
            img = pygame.image.load(self.pac_right_animation)
            img = pygame.transform.scale(img, (maze.psz, maze.psz))
            maze.pacman.image = img
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centerx -= settings.movement

        if self.pac_moving_up == True:
            maze.pacman.rect.centery -= settings.movement
            img = pygame.image.load(self.pac_up_animation)
            img = pygame.transform.scale(img, (maze.psz, maze.psz))
            maze.pacman.image = img
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centery += settings.movement

        if self.pac_moving_down == True:
            maze.pacman.rect.centery += settings.movement
            img = pygame.image.load(self.pac_down_animation)
            img = pygame.transform.scale(img, (maze.psz, maze.psz))
            maze.pacman.image = img
        if maze.pacman.rect.collidelist(maze.bricks) >= 0 or maze.pacman.rect.collidelist(maze.shields) >= 0:
            maze.pacman.rect.centery -= settings.movement

        tablet_collision = maze.pacman.rect.collidelist(maze.tablets)
        if tablet_collision >= 0:
            del maze.tablets[tablet_collision]

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