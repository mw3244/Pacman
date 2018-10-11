import pygame
import sys

def check_key_events(game_settings, screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

def update_screen(game_settings, screen):
    screen.fill(game_settings.bg_color)

    pygame.display.flip()