import pygame
from maze import Maze
from settings import Settings
from eventloop import EventLoop
from stats import Stats
from menuloop import MenuLoop

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Pacman Portal")
        screen = self.screen
        self.stats = Stats()
        self.mazefile = 'images/mazemap.txt'
        self.maze = Maze(screen, self.mazefile, 'square', 'shield', 'left_bigman_1', 'powerpill', 'tablet', 'up_clyde_1', 'up_pinky_1',
                         'up_inky_1', 'up_blinky_1', self.stats)
        file = open('highscore.txt', 'r')
        self.stats.high_score = int(file.read())
        file.close()

    def __str__(self): return 'Game(Pacman Portal), maze=' + str(self.maze) + ')'

    def play(self):
        while True:
            mloop = MenuLoop(self.screen, self.stats, finished = False, highscore_screen = False)
            while not mloop.finished:
                mloop.check_events()
                mloop.update()
                self.update_menu_screen(mloop)
                if mloop.highscore_screen == True:
                    while mloop.highscore_screen:
                        mloop.check_highscore_events()
                        mloop.update_highscore_screen()
                        self.update_highscore_screen(mloop)

            self.maze = Maze(self.screen, self.mazefile, 'square', 'shield', 'left_bigman_1', 'powerpill', 'tablet', 'up_clyde_1',
                             'up_pinky_1',
                             'up_inky_1', 'up_blinky_1', self.stats)
            eloop = EventLoop(self.maze, self.screen, finished = False)

            while not eloop.finished:
                eloop.check_events()
                eloop.update(self.settings, self.screen, self.stats)
                self.update_screen()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.maze.blitme()
        pygame.display.flip()
    def update_menu_screen(self, mloop):
        self.screen.fill(self.settings.bg_color)
        mloop.blitme()
        pygame.display.flip()
    def update_highscore_screen(self, mloop):
        self.screen.fill(self.settings.bg_color)
        mloop.blit2()
        pygame.display.flip()

game = Game()
game.play()