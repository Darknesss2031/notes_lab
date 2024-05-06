import sys
import pygame
import os
sys.path.append(os.path.abspath(__file__))
import menu


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    current_screen = menu.MenuScreen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        current_screen = current_screen.update()
        current_screen.draw()
