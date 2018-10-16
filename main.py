import pygame
from maze import Maze
from settings import Settings
from eventloop import EventLoop

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Pacman Portal")
        screen = self.screen
        mazefile = 'images/mazemap.txt'
        self.maze = Maze(screen, mazefile, 'square', 'shield', 'left_pac_1', 'powerpill', 'tablet', 'up_clyde_1', 'up_pinky_1',
                         'up_inky_1', 'up_blinky_1')

    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def play(self):
        eloop = EventLoop(finished = False)

        while not eloop.finished:
            eloop.check_events(self.maze)
            eloop.update(self.maze, self.settings)
            self.update_screen()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.maze.blitme()
        pygame.display.flip()

game = Game()
game.play()