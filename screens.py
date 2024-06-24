import sys

import pygame

from tools import ClassicButton, SwitchButton, GREEN, TextLabel, CheckBoxPair, ImageButton
import os
from notes_on_stave import GameProcess as NotesOnStaveGame
from notes_by_ear import GameProcess as NotesByEarGame
from piano import Piano
from stats import StatsRepository


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
            return StatsScreen()
        if setts:
            return SettingsScreen()
        return self


class NotesOnStaveScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.piano = Piano(self.screen)
        self.game = NotesOnStaveGame(self.screen, 3)
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
            return GameOverScreen(NotesOnStaveScreen, f"{self.game.correct} of {self.game.maxscore}")
        return self


class GameMenuScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.stave_btn = ClassicButton("Notes\non the stave", 120, 120, (106, 280), self.screen)
        self.ear_btn = ClassicButton("Notes by ear", 120, 120, (278, 280), self.screen)
        self.logo = pygame.image.load(os.path.join(os.getcwd(), "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500,200))
        self.back = ClassicButton("Back", 50, 30, (440, 460), self.screen)
        self.stave_setts = False
        self.ear_start = False
        self.next = self

    def draw(self):
        self.screen.fill(GREEN)
        self.clicked_stave = self.stave_btn.draw()
        self.clicked_ear = self.ear_btn.draw()
        self.clicked_back = self.back.draw()
        self.screen.blit(self.logo, (-20, 0))
        self.next = self.switch(self.clicked_stave, self.clicked_ear, self.clicked_back)
        pygame.display.update()
    
    def update(self):
        return self.next

    def switch(self, stave, ear, back):
        if stave:
            return NotesOnStaveScreen()
        if ear:
            return NotesByEarScreen()
        if back:
            return MenuScreen()
        return self


class GameOverScreen:

    def __init__(self, again_screen, score=""):
        self.screen = pygame.display.get_surface()
        self.retry_btn = ClassicButton("Try again", 200, 40, (150, 250), self.screen, 0)
        self.menu_btn = ClassicButton("Menu", 200, 40, (150, 300), self.screen, 0)
        self.label = TextLabel("GAME OVER!", 200, 50, (150, 100), self.screen, 50)
        self.again_screen = again_screen
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
            return self.again_screen()
        return self


class NotesByEarScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.piano = Piano(self.screen)
        self.game = NotesByEarGame(self.screen, 3)
        self.back = ClassicButton("Back", 50, 30, (440, 460), self.screen)
        self.next = self
        self.game.start_game()

    def draw(self):
        self.screen.fill(GREEN)
        if self.game.next_btn.draw():
            self.game.next_note()
        if self.game.retry_btn.draw():
            self.game.play_note()
        self.game.score.draw()
        self.game.answer.draw()
        back = self.back.draw()
        pressed_key = self.piano.draw()
        if pressed_key != None:
            self.game.process_key(pressed_key)
        self.next = self.switch(back, self.game.STOP)
        pygame.display.update()

    def update(self):
        return self.next
    
    def switch(self, back, finished):
        if back:
            self.game.end_game()
            return GameMenuScreen()
        if finished:
            self.game.end_game()
            return GameOverScreen(NotesByEarScreen, f"{self.game.correct} of {self.game.maxscore}")
        return self


class SettingsScreen:

    def __init__(self):
        self.screen = pygame.display.get_surface()
        size = 25
        shift = 30
        x = 50
        y = 80
        self.notes1 = 3
        self.notes2 = 3
        self.check_loc = CheckBoxPair(self.screen, x, y, size=size, shift=shift)
        self.next = self
        self.back = ClassicButton("Back", 50, 30, (440, 460), self.screen)
        self.apply = ClassicButton("Apply", 50, 30, (385, 460), self.screen)
        self.choose_loc = TextLabel("Choose the language", 500, 30, (0, 30), self.screen, font=30)
        self.en = TextLabel("English", 110, 30, (x + size + 10, y), self.screen, font=30)
        self.ru = TextLabel("Русский", 110, 30, (x + size + 10, y + size + shift), self.screen, font=30)
        self.choose_diff = TextLabel("Choose the number of notes for each game", 500, 30, (0, 190), self.screen, font=30)
        self.game1_label = TextLabel("Notes on stave:", 250, 30, (0, 250), self.screen, font=30)
        self.decrease1 = ClassicButton("-", 30, 30, (250, 250), self.screen)
        self.notes1_label = TextLabel(f"{self.notes1}", 30, 30, (280, 250), self.screen, font=30)
        self.increase1 = ClassicButton("+", 30, 30, (310, 250), self.screen)
        self.game2_label = TextLabel("Notes by ear:", 250, 30, (0, 310), self.screen, font=30)
        self.decrease2 = ClassicButton("-", 30, 30, (250, 310), self.screen)
        self.notes2_label = TextLabel(f"{self.notes2}", 30, 30, (280, 310), self.screen, font=30)
        self.increase2 = ClassicButton("+", 30, 30, (310, 310), self.screen)

    def draw(self):
        self.screen.fill(GREEN)
        self.check_loc.draw()
        self.choose_loc.draw()
        self.ru.draw()
        self.en.draw()
        self.choose_diff.draw()
        self.game1_label.draw()
        self.game2_label.draw()
        if self.decrease1.draw():
            if self.notes1 > 1:
                self.notes1 -= 1
        if self.increase1.draw():
            self.notes1 += 1
        self.notes1_label = TextLabel(f"{self.notes1}", 30, 30, (280, 250), self.screen, font=30)
        self.notes1_label.draw()
        if self.decrease2.draw():
            if self.notes2 > 1:
                self.notes2 -= 1
        if self.increase2.draw():
            self.notes2 += 1
        self.notes2_label = TextLabel(f"{self.notes2}", 30, 30, (280, 310), self.screen, font=30)
        self.notes2_label.draw()
        back = self.back.draw()
        apply = self.apply.draw()
        self.next = self.switch(back, apply)
        pygame.display.update()

    def update(self):
        return self.next

    def switch(self, back, apply):
        if back:
            return MenuScreen()
        if apply:
            return self
          
          
class StatsScreen:

    NEXT_BTN = os.path.join(os.getcwd(), "assets", "next.png")
    PREV_BTN = os.path.join(os.getcwd(), "assets", "prev.png")

    def __init__(self):
        self.offset = 0
        self.limit = 10
        self.screen = pygame.display.get_surface()
        self.stats = StatsRepository()
        data = self.stats.get_games(self.offset, self.limit)
        self.games_list = list(
            ClassicButton(f"{data[i][1]}        {data[i][2]}/{data[i][3]}        {data[i][4]}", 250, 30, (125, 100+i*28), self.screen, clickable=False, border=0) for i in range(len(data))
        )
        self.next = self
        self.current_page = 1
        self.name = TextLabel("Games History", 200, 30, (150, 60), self.screen)
        self.back = ClassicButton("Back", 50, 30, (440, 460), self.screen)
        self.total_pages = max(1, (self.stats.number_of_games()+self.limit-1) // self.limit)
        self.previous_btn = ImageButton(30, 30, (175, 420), self.screen, self.PREV_BTN, clickable=False)
        if self.total_pages == 1:
            self.next_btn = ImageButton(30, 30, (295, 420), self.screen, self.NEXT_BTN, clickable=False)
        else:
            self.next_btn = ImageButton(30, 30, (295, 420), self.screen, self.NEXT_BTN)
        self.pages_label = TextLabel(f"Page {self.current_page}/{self.total_pages}", 90, 30, (205, 420), self.screen, 30)

    def draw(self):
        self.screen.fill(GREEN)
        clicked_prev = self.previous_btn.draw()
        clicked_next = self.next_btn.draw()
        clicked_back = self.back.draw()
        self.name.draw()
        if self.current_page != 1 and clicked_prev:
            self.previous_page()
        elif self.current_page != self.total_pages and clicked_next:
            self.next_page()
        for label in self.games_list:
            label.draw()
        self.pages_label.draw()
        self.next = self.switch(clicked_back)
        pygame.display.update()

    def next_page(self):
        self.offset += self.limit
        self.current_page += 1
        if self.current_page == 2:
            self.previous_btn = ImageButton(30, 30, (175, 420), self.screen, self.PREV_BTN)
        if self.current_page == self.total_pages:
            self.next_btn = ImageButton(30, 30, (295, 420), self.screen, self.NEXT_BTN, clickable=False)
        data = self.stats.get_games(self.offset, self.limit)
        self.games_list = list(
            ClassicButton(f"{data[i][1]}        {data[i][2]}/{data[i][3]}        {data[i][4]}", 250, 30, (125, 100+i*28), self.screen, clickable=False, border=0) for i in range(len(data))
        )
        self.pages_label = TextLabel(f"Page {self.current_page}/{self.total_pages}", 90, 30, (205, 420), self.screen, 30)

    def previous_page(self):
        self.offset -= self.limit
        self.current_page -= 1
        if self.current_page == 1:
            self.previous_btn = ImageButton(30, 30, (175, 420), self.screen, self.PREV_BTN, clickable=False)
        if self.current_page == self.total_pages - 1:
            self.next_btn = ImageButton(30, 30, (295, 420), self.screen, self.NEXT_BTN)
        data = self.stats.get_games(self.offset, self.limit)
        self.games_list = list(
            ClassicButton(f"{data[i][1]}        {data[i][2]}/{data[i][3]}        {data[i][4]}", 250, 30, (125, 100+i*28), self.screen, clickable=False, border=0) for i in range(len(data))
        )
        self.pages_label = TextLabel(f"Page {self.current_page}/{self.total_pages}", 90, 30, (205, 420), self.screen, 30)

    def update(self):
        return self.next

    def switch(self, back):
        if back:
            return MenuScreen()
        return self