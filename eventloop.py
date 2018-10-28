import pygame
from settings import Settings
import sys
import time
from imagerect import ImageRect
from dijkstra import Dijkstra
from button import Text
from stats import Stats
import math
import random

class EventLoop:
    def __init__(self, maze, screen, finished):
        self.settings = Settings()
        self.maze = maze
        self.finished = finished
        self.screen = screen

        self.life_up_check = 0

        self.pac_moving_left = False
        self.pac_moving_right = False
        self.pac_moving_up = False
        self.pac_moving_down = False
        self.pac_left_animation = 'images/left_bigman_1.png'
        self.pac_right_animation = 'images/right_bigman_1.png'
        self.pac_up_animation = 'images/up_bigman_1.png'
        self.pac_down_animation = 'images/down_bigman_1.png'

        self.clyde_up_1_img = pygame.image.load('images/up_clyde_1.png')
        self.clyde_up_1_img = pygame.transform.scale(self.clyde_up_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_up_2_img = pygame.image.load('images/up_clyde_2.png')
        self.clyde_up_2_img = pygame.transform.scale(self.clyde_up_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_left_1_img = pygame.image.load('images/left_clyde_1.png')
        self.clyde_left_1_img = pygame.transform.scale(self.clyde_left_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_left_2_img = pygame.image.load('images/left_clyde_2.png')
        self.clyde_left_2_img = pygame.transform.scale(self.clyde_left_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_right_1_img = pygame.image.load('images/right_clyde_1.png')
        self.clyde_right_1_img = pygame.transform.scale(self.clyde_right_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_right_2_img = pygame.image.load('images/right_clyde_2.png')
        self.clyde_right_2_img = pygame.transform.scale(self.clyde_right_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_down_1_img = pygame.image.load('images/down_clyde_1.png')
        self.clyde_down_1_img = pygame.transform.scale(self.clyde_down_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_down_2_img = pygame.image.load('images/down_clyde_2.png')
        self.clyde_down_2_img = pygame.transform.scale(self.clyde_down_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.clyde_up_img = self.clyde_up_1_img
        self.clyde_down_img = self.clyde_down_1_img
        self.clyde_left_img = self.clyde_left_1_img
        self.clyde_right_img = self.clyde_right_1_img

        self.pinky_up_1_img = pygame.image.load('images/up_pinky_1.png')
        self.pinky_up_1_img = pygame.transform.scale(self.pinky_up_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_up_2_img = pygame.image.load('images/up_pinky_2.png')
        self.pinky_up_2_img = pygame.transform.scale(self.pinky_up_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_left_1_img = pygame.image.load('images/left_pinky_1.png')
        self.pinky_left_1_img = pygame.transform.scale(self.pinky_left_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_left_2_img = pygame.image.load('images/left_pinky_2.png')
        self.pinky_left_2_img = pygame.transform.scale(self.pinky_left_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_right_1_img = pygame.image.load('images/right_pinky_1.png')
        self.pinky_right_1_img = pygame.transform.scale(self.pinky_right_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_right_2_img = pygame.image.load('images/right_pinky_2.png')
        self.pinky_right_2_img = pygame.transform.scale(self.pinky_right_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_down_1_img = pygame.image.load('images/down_pinky_1.png')
        self.pinky_down_1_img = pygame.transform.scale(self.pinky_down_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_down_2_img = pygame.image.load('images/down_pinky_2.png')
        self.pinky_down_2_img = pygame.transform.scale(self.pinky_down_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.pinky_up_img = self.pinky_up_1_img
        self.pinky_down_img = self.pinky_down_1_img
        self.pinky_left_img = self.pinky_left_1_img
        self.pinky_right_img = self.pinky_right_1_img

        self.inky_up_1_img = pygame.image.load('images/up_inky_1.png')
        self.inky_up_1_img = pygame.transform.scale(self.inky_up_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_up_2_img = pygame.image.load('images/up_inky_2.png')
        self.inky_up_2_img = pygame.transform.scale(self.inky_up_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_left_1_img = pygame.image.load('images/left_inky_1.png')
        self.inky_left_1_img = pygame.transform.scale(self.inky_left_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_left_2_img = pygame.image.load('images/left_inky_2.png')
        self.inky_left_2_img = pygame.transform.scale(self.inky_left_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_right_1_img = pygame.image.load('images/right_inky_1.png')
        self.inky_right_1_img = pygame.transform.scale(self.inky_right_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_right_2_img = pygame.image.load('images/right_inky_2.png')
        self.inky_right_2_img = pygame.transform.scale(self.inky_right_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_down_1_img = pygame.image.load('images/down_inky_1.png')
        self.inky_down_1_img = pygame.transform.scale(self.inky_down_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_down_2_img = pygame.image.load('images/down_inky_2.png')
        self.inky_down_2_img = pygame.transform.scale(self.inky_down_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.inky_up_img = self.inky_up_1_img
        self.inky_down_img = self.inky_down_1_img
        self.inky_left_img = self.inky_left_1_img
        self.inky_right_img = self.inky_right_1_img

        self.blinky_up_1_img = pygame.image.load('images/up_blinky_1.png')
        self.blinky_up_1_img = pygame.transform.scale(self.blinky_up_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_up_2_img = pygame.image.load('images/up_blinky_2.png')
        self.blinky_up_2_img = pygame.transform.scale(self.blinky_up_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_left_1_img = pygame.image.load('images/left_blinky_1.png')
        self.blinky_left_1_img = pygame.transform.scale(self.blinky_left_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_left_2_img = pygame.image.load('images/left_blinky_2.png')
        self.blinky_left_2_img = pygame.transform.scale(self.blinky_left_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_right_1_img = pygame.image.load('images/right_blinky_1.png')
        self.blinky_right_1_img = pygame.transform.scale(self.blinky_right_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_right_2_img = pygame.image.load('images/right_blinky_2.png')
        self.blinky_right_2_img = pygame.transform.scale(self.blinky_right_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_down_1_img = pygame.image.load('images/down_blinky_1.png')
        self.blinky_down_1_img = pygame.transform.scale(self.blinky_down_1_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_down_2_img = pygame.image.load('images/down_blinky_2.png')
        self.blinky_down_2_img = pygame.transform.scale(self.blinky_down_2_img, (self.maze.sz * 2, self.maze.sz * 2))
        self.blinky_up_img = self.blinky_up_1_img
        self.blinky_down_img = self.blinky_down_1_img
        self.blinky_left_img = self.blinky_left_1_img
        self.blinky_right_img = self.blinky_right_1_img

        self.ghost_animation_queue = 0

        self.pac_animation_clock = self.settings.pac_animation_clock
        self.search_clock = self.settings.search_clock
        self.clyde_path = []
        self.pinky_path = []
        self.inky_path = []
        self.blinky_path = []
        self.ghost_move_OK = False
        self.fleeing = False
        self.fleeing_clock = self.settings.fleeing_clock

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

    def update(self, settings, screen, stats):
        if (self.maze.pacman.rect.colliderect(self.maze.clyde.rect) or self.maze.pacman.rect.colliderect(self.maze.pinky.rect)
        or self.maze.pacman.rect.colliderect(self.maze.inky.rect) or self.maze.pacman.rect.colliderect(self.maze.blinky.rect))\
        and not self.fleeing:
            img = pygame.image.load('images/pac_death_1.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_2.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_3.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_4.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_5.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_6.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_7.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_8.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_9.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_10.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_11.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(0.1)
            img = pygame.image.load('images/pac_death_12.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.maze.blitme()
            pygame.display.flip()
            time.sleep(1)

            stats.lives -= 1
            if stats.lives == 0:
                print("Game over!")
            self.maze.pacman.rect.x = self.maze.pacman_init_x
            self.maze.pacman.rect.y = self.maze.pacman_init_y
            self.maze.clyde.rect.x = self.maze.clyde_init_x
            self.maze.clyde.rect.y = self.maze.clyde_init_y
            self.maze.pinky.rect.x = self.maze.pinky_init_x
            self.maze.pinky.rect.y = self.maze.pinky_init_y
            self.maze.inky.rect.x = self.maze.inky_init_x
            self.maze.inky.rect.y = self.maze.inky_init_y
            self.maze.blinky.rect.x = self.maze.blinky_init_x
            self.maze.blinky.rect.y = self.maze.blinky_init_y
            self.clyde_path = []
            self.pinky_path = []
            self.inky_path = []
            self.blinky_path = []
            img = pygame.image.load('images/left_bigman_1.png')
            img = pygame.transform.scale(img, (self.maze.psz, self.maze.psz))
            self.maze.pacman.image = img
            self.screen.blit(self.maze.pacman.image, self.maze.pacman.rect)
            pygame.display.flip()
            time.sleep(2)

        if not self.maze.tablets and not self.maze.powerpills:
            self.maze.shields = []
            self.maze.bricks = []
            self.fleeing = False
            self.maze.build()
            time.sleep(2)

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
            stats.score += 20
            self.life_up_check += 20

        powerpill_collision = self.maze.pacman.rect.collidelist(self.maze.powerpills)
        if powerpill_collision >= 0:
            del self.maze.powerpills[powerpill_collision]
            self.fleeing = True
            self.fleeing_clock = self.settings.fleeing_clock



        self.pac_animation_clock -= 1

        if self.pac_animation_clock <= 0:
            if self.pac_left_animation == 'images/bigman_3.png':
                self.pac_left_animation = 'images/left_bigman_1.png'
                self.pac_right_animation = 'images/right_bigman_1.png'
                self.pac_up_animation = 'images/up_bigman_1.png'
                self.pac_down_animation = 'images/down_bigman_1.png'

            elif self.pac_left_animation == 'images/left_bigman_2.png':
                self.pac_left_animation = 'images/bigman_3.png'
                self.pac_right_animation = 'images/bigman_3.png'
                self.pac_up_animation = 'images/bigman_3.png'
                self.pac_down_animation = 'images/bigman_3.png'

            elif self.pac_left_animation == 'images/left_bigman_1.png':
                self.pac_left_animation = 'images/left_bigman_2.png'
                self.pac_right_animation = 'images/right_bigman_2.png'
                self.pac_up_animation = 'images/up_bigman_2.png'
                self.pac_down_animation = 'images/down_bigman_2.png'

            if self.ghost_animation_queue == 0:
                self.clyde_up_img = self.clyde_up_2_img
                self.clyde_down_img = self.clyde_down_2_img
                self.clyde_left_img = self.clyde_left_2_img
                self.clyde_right_img = self.clyde_right_2_img
                self.pinky_up_img = self.pinky_up_2_img
                self.pinky_down_img = self.pinky_down_2_img
                self.pinky_left_img = self.pinky_left_2_img
                self.pinky_right_img = self.pinky_right_2_img
                self.inky_up_img = self.inky_up_2_img
                self.inky_down_img = self.inky_down_2_img
                self.inky_left_img = self.inky_left_2_img
                self.inky_right_img = self.inky_right_2_img
                self.blinky_up_img = self.blinky_up_2_img
                self.blinky_down_img = self.blinky_down_2_img
                self.blinky_left_img = self.blinky_left_2_img
                self.blinky_right_img = self.blinky_right_2_img

                self.ghost_animation_queue += 1
            elif self.ghost_animation_queue == 1:
                self.clyde_up_img = self.clyde_up_1_img
                self.clyde_down_img = self.clyde_down_1_img
                self.clyde_left_img = self.clyde_left_1_img
                self.clyde_right_img = self.clyde_right_1_img
                self.pinky_up_img = self.pinky_up_1_img
                self.pinky_down_img = self.pinky_down_1_img
                self.pinky_left_img = self.pinky_left_1_img
                self.pinky_right_img = self.pinky_right_1_img
                self.inky_up_img = self.inky_up_1_img
                self.inky_down_img = self.inky_down_1_img
                self.inky_left_img = self.inky_left_1_img
                self.inky_right_img = self.inky_right_1_img
                self.blinky_up_img = self.blinky_up_1_img
                self.blinky_down_img = self.blinky_down_1_img
                self.blinky_left_img = self.blinky_left_1_img
                self.blinky_right_img = self.blinky_right_1_img

                self.ghost_animation_queue -= 1



            self.pac_animation_clock = self.settings.pac_animation_clock

        self.search_clock -= 1
        self.fleeing_clock -= 1
        if self.fleeing_clock <= 0:
            self.fleeing = False

        if self.search_clock == 150 and self.fleeing:
            random_clyde_path = random.choice(list(self.maze.nodeDict.keys()))
            clydeNode = self.getObjectNode("clyde")
            self.clyde_path = Dijkstra(clydeNode, random_clyde_path, self.maze.nodeDict)
        if self.search_clock == 100 and self.fleeing:
            random_pinky_path = random.choice(list(self.maze.nodeDict.keys()))
            pinkyNode = self.getObjectNode("pinky")
            self.pinky_path = Dijkstra(pinkyNode, random_pinky_path, self.maze.nodeDict)
        if self.search_clock == 50 and self.fleeing:
            random_inky_path = random.choice(list(self.maze.nodeDict.keys()))
            inkyNode = self.getObjectNode("inky")
            self.inky_path = Dijkstra(inkyNode, random_inky_path, self.maze.nodeDict)
        if self.search_clock <= 0 and self.fleeing:
            random_blinky_path = random.choice(list(self.maze.nodeDict.keys()))
            blinkyNode = self.getObjectNode("blinky")
            self.blinky_path = Dijkstra(blinkyNode, random_blinky_path, self.maze.nodeDict)
            self.search_clock = self.settings.search_clock

        if self.search_clock == 150 and not self.fleeing:
            pacNode = self.getObjectNode("pacman")
            clydeNode = self.getObjectNode("clyde")
            self.clyde_path = Dijkstra(clydeNode, pacNode, self.maze.nodeDict)
        if self.search_clock == 100 and not self.fleeing:
            pacNode = self.getObjectNode("pacman")
            pinkyNode = self.getObjectNode("pinky")
            self.pinky_path = Dijkstra(pinkyNode, pacNode, self.maze.nodeDict)
        if self.search_clock == 50 and not self.fleeing:
            pacNode = self.getObjectNode("pacman")
            inkyNode = self.getObjectNode("inky")
            self.inky_path = Dijkstra(inkyNode, pacNode, self.maze.nodeDict)
        if self.search_clock <= 0 and not self.fleeing:
            pacNode = self.getObjectNode("pacman")
            blinkyNode = self.getObjectNode("blinky")
            self.blinky_path = Dijkstra(blinkyNode, pacNode, self.maze.nodeDict)
            self.search_clock = self.settings.search_clock

        self.updateGhost("clyde")
        self.updateGhost("pinky")
        self.updateGhost("inky")
        self.updateGhost("blinky")

        if self.life_up_check >= 10000:
            stats.lives += 1
            self.life_up_check = 0

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
                if identifier == "clyde":
                    self.maze.clyde.image = self.clyde_right_img
                elif identifier == "pinky":
                    self.maze.pinky.image = self.pinky_right_img
                elif identifier == "inky":
                    self.maze.inky.image = self.inky_right_img
                elif identifier == "blinky":
                    self.maze.blinky.image = self.blinky_right_img
            elif XDest < xObj:
                xObj-= self.settings.ghost_movement
                if identifier == "clyde":
                    self.maze.clyde.image = self.clyde_left_img
                elif identifier == "pinky":
                    self.maze.pinky.image = self.pinky_left_img
                elif identifier == "inky":
                    self.maze.inky.image = self.inky_left_img
                elif identifier == "blinky":
                    self.maze.blinky.image = self.blinky_left_img
            if YDest > yObj:
                yObj+= self.settings.ghost_movement
                if identifier == "clyde":
                    self.maze.clyde.image = self.clyde_down_img
                elif identifier == "pinky":
                    self.maze.pinky.image = self.pinky_down_img
                elif identifier == "inky":
                    self.maze.inky.image = self.inky_down_img
                elif identifier == "blinky":
                    self.maze.blinky.image = self.blinky_down_img
            elif YDest < yObj:
                yObj-= self.settings.ghost_movement
                if identifier == "clyde":
                    self.maze.clyde.image = self.clyde_up_img
                elif identifier == "pinky":
                    self.maze.pinky.image = self.pinky_up_img
                elif identifier == "inky":
                    self.maze.inky.image = self.inky_up_img
                elif identifier == "blinky":
                    self.maze.blinky.image = self.blinky_up_img

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
