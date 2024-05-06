"""This file contains game choosing logic"""
import pygame
import os
from notes_by_ear import NotesByEarScreen


class GameMenuButton:

    TEXT_INTERVAL = 16

    def __init__(self, text, width, height, pos, screen):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = (0, 100, 100)
        self.pressed = False
        self.frame = 2
        self.screen = screen
        self.text_surf, self.text_rect = list(), list()
        self.text = text.split("\n")
        begin = -((len(self.text)//2)*self.TEXT_INTERVAL - ((len(self.text)+1)%2) * self.TEXT_INTERVAL//2)
        for i, line in enumerate(self.text):
            self.text_surf.append(m := pygame.font.Font(None, 20).render(line, True, '#000000'))
            self.text_rect.append(m.get_rect(centerx=self.top_rect.centerx, centery=self.top_rect.centery+begin))
            begin += self.TEXT_INTERVAL

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, self.frame, border_radius=6)
        for surf, rect in zip(self.text_surf, self.text_rect):
            self.screen.blit(surf, rect)
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


class GameMenuScreen:

    def __init__(self):
        self.screen = pygame.display.set_mode((500, 500))
        self.stave_btn = GameMenuButton("Notes\non the stave", 120, 120, (46, 230), self.screen)
        self.neck_btn = GameMenuButton("Notes\non the neck", 120, 120, (192, 230), self.screen)
        self.ear_btn = GameMenuButton("Notes by ear", 120, 120, (338, 230), self.screen)
        self.qcof_btn = GameMenuButton("Quarto circle\nof fifths", 120, 120, (125, 370), self.screen)
        self.key_btn = GameMenuButton("Key of a melody", 120, 120, (275, 370), self.screen)
        self.logo = pygame.image.load(os.path.join(os.getcwd(), "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500,200))
        self.stave_setts = False
        self.neck_stats = False
        self.ear_start = False
        self.qcof_start = False
        self.key_start = False
        self.next = self

    def draw(self):
        self.screen.fill((0, 240, 100))
        self.clicked_stave = self.stave_btn.draw()
        self.clicked_neck = self.neck_btn.draw()
        self.clicked_ear = self.ear_btn.draw()
        self.clicked_qcof = self.qcof_btn.draw()
        self.clicked_key = self.key_btn.draw()
        self.screen.blit(self.logo, (-20, 0))
        self.next = self.switch(self.clicked_stave, self.clicked_neck, self.clicked_ear, self.clicked_qcof, self.clicked_key)
        pygame.display.update()
    
    def update(self):
        return self.next

    def switch(self, stave, neck, ear, qcof, key):
        if stave:
            return self
        if neck:
            return self
        if ear:
            return NotesByEarScreen()
        if qcof:
            return self
        if key:
            return self
        return self