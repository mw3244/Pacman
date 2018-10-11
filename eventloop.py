import pygame
import sys

class EventLoop:
    def __init__(self, finished):
        self.finished = finished

    def __str__(self):
        return 'eventloop, finished= ' + str(self.finished) + ')'

    @staticmethod
    def check_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()