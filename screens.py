import pygame
from tools import ClassicButton, SwitchButton, GREEN, TextLabel
import os
from notes_on_stave import GameProcess
from piano import Piano


class MenuScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.start_btn = ClassicButton("Start", 200, 40, (150, 230), self.screen, 0)
        self.stats_btn = ClassicButton("Statistics", 200, 40, (150, 280), self.screen, 0)
        self.setts_btn = ClassicButton("Settings", 200, 40, (150, 330), self.screen, 0)
        self.logo = pygame.image.load(os.path.join(os.getcwd(), "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500,200))
        self.clicked_setts = False
        self.clicked_stats = False
        self.clicked_start = False
        self.next = self

    def draw(self):
        self.screen.fill(GREEN)
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


class NotesOnStaveScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.piano = Piano(self.screen)
        self.game = GameProcess(self.screen, 3)
        self.game.start_game()
        self.switch_btn = SwitchButton(50, 20, (225, 260), self.screen,
                                       os.path.join(os.getcwd(), "assets", "key.png"),
                                       os.path.join(os.getcwd(), "assets", "bass.png"))
        self.back = ClassicButton("Back", 50, 30, (440, 460), self.screen)
        self.next = self

    def draw(self):
        self.screen.fill(GREEN)
        pressed_key = self.piano.draw()
        if pressed_key != None:
            #print(pressed_key)
            self.game.process_key(pressed_key)
        back_clicked = self.back.draw()
        if self.switch_btn.draw():
            self.game.change_mode()
        self.game.stave.draw()
        self.game.score.draw()
        finished = self.game.STOP
        self.next = self.switch(back_clicked, finished)
        pygame.display.update()

    def update(self):
        return self.next

    def switch(self, back, finished):
        if back:
            self.game.end_game()
            return GameMenuScreen()
        if finished:
            self.game.end_game()
            return GameOverScreen(f"{self.game.correct} of {self.game.maxscore}")
        return self


class GameMenuScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.stave_btn = ClassicButton("Notes\non the stave", 120, 120, (46, 230), self.screen)
        self.neck_btn = ClassicButton("Notes\non the neck", 120, 120, (192, 230), self.screen)
        self.ear_btn = ClassicButton("Notes by ear", 120, 120, (338, 230), self.screen)
        self.qcof_btn = ClassicButton("Quarto circle\nof fifths", 120, 120, (125, 370), self.screen)
        self.key_btn = ClassicButton("Key of a melody", 120, 120, (275, 370), self.screen)
        self.logo = pygame.image.load(os.path.join(os.getcwd(), "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500,200))
        self.back = ClassicButton("Back", 50, 30, (440, 460), self.screen)
        self.stave_setts = False
        self.neck_stats = False
        self.ear_start = False
        self.qcof_start = False
        self.key_start = False
        self.next = self

    def draw(self):
        self.screen.fill(GREEN)
        self.clicked_stave = self.stave_btn.draw()
        self.clicked_neck = self.neck_btn.draw()
        self.clicked_ear = self.ear_btn.draw()
        self.clicked_qcof = self.qcof_btn.draw()
        self.clicked_key = self.key_btn.draw()
        self.clicked_back = self.back.draw()
        self.screen.blit(self.logo, (-20, 0))
        self.next = self.switch(self.clicked_stave, self.clicked_neck, self.clicked_ear, self.clicked_qcof, self.clicked_key, self.clicked_back)
        pygame.display.update()
    
    def update(self):
        return self.next

    def switch(self, stave, neck, ear, qcof, key, back):
        if stave:
            return NotesOnStaveScreen()
        if neck:
            return self
        if ear:
            return self
        if qcof:
            return self
        if key:
            return self
        if back:
            return MenuScreen()
        return self


class GameOverScreen:

    def __init__(self, score=""):
        self.screen = pygame.display.get_surface()
        self.retry_btn = ClassicButton("Try again", 200, 40, (150, 250), self.screen, 0)
        self.menu_btn = ClassicButton("Menu", 200, 40, (150, 300), self.screen, 0)
        self.label = TextLabel("GAME OVER!", 200, 50, (150, 100), self.screen, 50)
        self.results = TextLabel(f"Your score is: {score}", 200, 30, (150, 200), self.screen, 20)

    def draw(self):
        self.screen.fill(GREEN)
        self.clicked_menu = self.menu_btn.draw()
        self.clicked_retry = self.retry_btn.draw()
        self.label.draw()
        self.results.draw()
        self.next = self.switch(self.clicked_menu, self.clicked_retry)
        pygame.display.update()

    def update(self):
        return self.next

    def switch(self, menu, retry):
        if menu:
            return GameMenuScreen()
        if retry:
            return NotesOnStaveScreen()
        return self