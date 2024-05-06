"""This file contains main menu logic"""
import pygame
import os
from game_selection import GameMenuScreen


class MenuButton:

    def __init__(self, text, width, height, pos, screen):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (0, 100, 100)
        self.pressed = False
        self.frame = 2
        self.screen = screen
        self.text_surf = pygame.font.Font(None, 20).render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, self.frame)
        self.screen.blit(self.text_surf, self.text_rect)
        if self.covered():
            return True
        return False
    
    def covered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                    self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True

            if self.pressed:
                self.top_color = (0, 50, 255)
            else:
                self.top_color = (0, 100, 200)
            self.frame = 0
        else:
            self.top_color = (0, 100, 100)
            self.frame = 2
        return False


class MenuScreen:

    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        self.start_btn = MenuButton("Start", 200, 40, (150, 230), self.screen)
        self.stats_btn = MenuButton("Statistics", 200, 40, (150, 280), self.screen)
        self.setts_btn = MenuButton("Settings", 200, 40, (150, 330), self.screen)
        self.logo = pygame.image.load(os.path.join(os.getcwd(), "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500,200))
        self.clicked_setts = False
        self.clicked_stats = False
        self.clicked_start = False
        self.next = self

    def draw(self):
        self.screen.fill((0, 240, 100))
        self.clicked_start = self.start_btn.draw()
        self.clicked_stats = self.stats_btn.draw()
        self.clicked_setts = self.setts_btn.draw()
        self.screen.blit(self.logo, (-20, 0))
        self.next = self.switch(self.clicked_start, self.clicked_stats, self.clicked_setts)
        pygame.display.update()

    def update(self):
        return self.next

    def switch(self, start, stats, setts):
        if start:
            return GameMenuScreen()
        if stats:
            return self
        if setts:
            return self
        return self
        