import pygame
class Stats:
    def __init__(self):
        self.score = 0
        self.high_score = 0
        self.lives = 3
        self.score_font = pygame.font.SysFont("monospace", 96)
        self.score_label = self.score_font.render(str(self.score), True, (255, 255, 255))