"""This module is the main module of the notes_lab game."""
import sys
import pygame
import os
from .src.screens import MenuScreen
from .src.stats import StatsRepository

sys.path.append(os.path.abspath(__file__))


if __name__ == '__main__':
    pygame.init()
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "db")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "db"))
    screen = pygame.display.set_mode((500, 500))
    current_screen = MenuScreen()
    StatsRepository().setup()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        current_screen = current_screen.update()
        current_screen.draw()
