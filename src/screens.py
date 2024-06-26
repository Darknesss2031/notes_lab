"""This file contains screens GUI."""

import pygame

from .tools import (ClassicButton, SwitchButton, GREEN,
                    TextLabel, CheckBoxPair, ImageButton)
import os
import gettext
from .notes_on_stave import GameProcess as NotesOnStaveGame
from .notes_by_ear import GameProcess as NotesByEarGame
from .piano import Piano
from .stats import StatsRepository

print(os.getcwd())

LOCALES = {
    "ru": gettext.translation("loc",
                              os.path.join(os.path.dirname(__file__), "loc"),
                              ["ru"], fallback=False),
    "en": gettext.NullTranslations()
}


def _(text):
    """Translate strings."""
    return LOCALES[Settings.localization].gettext(text)


class Settings:
    """Class to storage the settings of the game."""

    localization = "en"
    notes_on_stave = 3
    notes_by_ear = 3

    @classmethod
    def set_notes_on_stave(cls, n):
        """Call to set the number of notes in notes on the stave game."""
        cls.notes_on_stave = n

    @classmethod
    def set_notes_by_ear(cls, n):
        """Call to set the number of notes in notes by ear game."""
        cls.notes_by_ear = n

    @classmethod
    def set_localization(cls, loc):
        """Call to set the localization game."""
        cls.localization = loc


class MenuScreen:
    """Class representing the screen of the menu."""

    def __init__(self):
        """Initialise function for menu screen class."""
        self.screen = pygame.display.get_surface()
        self.start_btn = ClassicButton(_("Start"), 200,
                                       40, (150, 230), self.screen, 0)
        self.stats_btn = ClassicButton(_("Statistics"), 200,
                                       40, (150, 280), self.screen, 0)
        self.setts_btn = ClassicButton(_("Settings"), 200,
                                       40, (150, 330), self.screen, 0)
        self.logo = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                   "..", "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500, 200))
        self.clicked_setts = False
        self.clicked_stats = False
        self.clicked_start = False
        self.next = self

    def draw(self):
        """Call to draw the menu screen."""
        self.screen.fill(GREEN)
        self.clicked_start = self.start_btn.draw()
        self.clicked_stats = self.stats_btn.draw()
        self.clicked_setts = self.setts_btn.draw()
        self.screen.blit(self.logo, (-20, 0))
        self.next = self.switch(self.clicked_start,
                                self.clicked_stats, self.clicked_setts)
        pygame.display.update()

    def update(self):
        """Call to update the menu screen."""
        return self.next

    def switch(self, start, stats, setts):
        """Call to switch the screen."""
        if start:
            return GameMenuScreen()
        if stats:
            return StatsScreen()
        if setts:
            return SettingsScreen()
        return self


class NotesOnStaveScreen:
    """Class represents the screen of notes on stave game."""

    def __init__(self):
        """Initialise function for notes on the stave screen."""
        self.screen = pygame.display.get_surface()
        self.piano = Piano(self.screen)
        self.game = NotesOnStaveGame(self.screen, Settings.notes_on_stave)
        self.game.start_game()
        self.switch_btn = SwitchButton(50, 20, (225, 260),
                                       self.screen,
                                       os.path.join(os.path.dirname(__file__),
                                                    "..", "assets", "key.png"),
                                       os.path.join(os.path.dirname(__file__),
                                                    "..", "assets", "bass.png"))
        self.back = ClassicButton(_("Back"), 50, 30, (440, 460), self.screen)
        self.next = self

    def draw(self):
        """Call to draw the notes on stave screen."""
        self.screen.fill(GREEN)
        pressed_key = self.piano.draw()
        if pressed_key is not None:
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
        """Call to update the notes on the stave screen."""
        return self.next

    def switch(self, back, finished):
        """Call to switch the screen."""
        if back:
            self.game.end_game()
            return GameMenuScreen()
        if finished:
            self.game.end_game()
            return GameOverScreen(NotesOnStaveScreen,
                                  _("{} of {}").format(self.game.correct,
                                                       self.game.maxscore))
        return self


class GameMenuScreen:
    """Class represents the screen of game menu."""

    def __init__(self):
        """Initialise function for the game menu screen class."""
        self.screen = pygame.display.get_surface()
        self.stave_btn = ClassicButton(_("Notes\non the stave"),
                                       120, 120, (106, 280), self.screen)
        self.ear_btn = ClassicButton(_("Notes by ear"),
                                     120, 120, (278, 280), self.screen)
        self.logo = pygame.image.load(os.path.join(os.path.dirname(__file__),
                                                   "..", "assets", "logo.png"))
        self.logo = pygame.transform.scale(self.logo, (500, 200))
        self.back = ClassicButton(_("Back"), 50, 30, (440, 460), self.screen)
        self.stave_setts = False
        self.ear_start = False
        self.next = self

    def draw(self):
        """Call to draw the game menu screen."""
        self.screen.fill(GREEN)
        self.clicked_stave = self.stave_btn.draw()
        self.clicked_ear = self.ear_btn.draw()
        self.clicked_back = self.back.draw()
        self.screen.blit(self.logo, (-20, 0))
        self.next = self.switch(self.clicked_stave,
                                self.clicked_ear, self.clicked_back)
        pygame.display.update()

    def update(self):
        """Call to update the game menu screen."""
        return self.next

    def switch(self, stave, ear, back):
        """Call to switch the screen."""
        if stave:
            return NotesOnStaveScreen()
        if ear:
            return NotesByEarScreen()
        if back:
            return MenuScreen()
        return self


class GameOverScreen:
    """Class represents the screen of the game ending."""

    def __init__(self, again_screen, score=""):
        """Initialise function for game over screen."""
        self.screen = pygame.display.get_surface()
        self.retry_btn = ClassicButton(_("Try again"),
                                       200, 40, (150, 250),
                                       self.screen, 0)
        self.menu_btn = ClassicButton(_("Menu"),
                                      200, 40, (150, 300),
                                      self.screen, 0)
        self.label = TextLabel(_("GAME OVER!"),
                               200, 50, (150, 100),
                               self.screen, 50)
        self.again_screen = again_screen
        self.results = TextLabel(_("Your score is: {}").format(score),
                                 200, 30, (150, 200),
                                 self.screen, 20)

    def draw(self):
        """Call to draw game over screen."""
        self.screen.fill(GREEN)
        self.clicked_menu = self.menu_btn.draw()
        self.clicked_retry = self.retry_btn.draw()
        self.label.draw()
        self.results.draw()
        self.next = self.switch(self.clicked_menu, self.clicked_retry)
        pygame.display.update()

    def update(self):
        """Call to update the game over screen."""
        return self.next

    def switch(self, menu, retry):
        """Call to switch the screen."""
        if menu:
            return GameMenuScreen()
        if retry:
            return self.again_screen()
        return self


class NotesByEarScreen:
    """Class represents the screen of the notes by ear game."""

    def __init__(self):
        """Initialise function for the notes by ear screen."""
        self.screen = pygame.display.get_surface()
        self.piano = Piano(self.screen)
        self.game = NotesByEarGame(self.screen,
                                   Settings.notes_by_ear,
                                   loc=Settings.localization)
        self.back = ClassicButton(_("Back"), 50, 30, (440, 460), self.screen)
        self.next = self
        self.game.start_game()

    def draw(self):
        """Call to draw the notes by ear screen."""
        self.screen.fill(GREEN)
        if self.game.next_btn.draw():
            self.game.next_note()
        if self.game.retry_btn.draw():
            self.game.play_note()
        self.game.score.draw()
        self.game.answer.draw()
        back = self.back.draw()
        pressed_key = self.piano.draw()
        if pressed_key is not None:
            self.game.process_key(pressed_key)
        self.next = self.switch(back, self.game.STOP)
        pygame.display.update()

    def update(self):
        """Call to update the notes by ear screen."""
        return self.next

    def switch(self, back, finished):
        """Call to switch the screen."""
        if back:
            self.game.end_game()
            return GameMenuScreen()
        if finished:
            self.game.end_game()
            return GameOverScreen(NotesByEarScreen,
                                  _("{} of {}").format(self.game.correct,
                                                       self.game.maxscore))
        return self


class SettingsScreen:
    """Class represents the screen of the settings."""

    def __init__(self):
        """Initialise function for settings screen class."""
        self.screen = pygame.display.get_surface()
        size = 25
        shift = 30
        x = 50
        y = 80
        self.notes1 = Settings.notes_on_stave
        self.notes2 = Settings.notes_by_ear
        if Settings.localization == "en":
            self.check_loc = CheckBoxPair(self.screen,
                                          x, y, size=size, shift=shift)
        else:
            self.check_loc = CheckBoxPair(self.screen,
                                          x, y, size=size, shift=shift,
                                          first_check=2)
        self.next = self
        self.back = ClassicButton(_("Back"), 50, 30,
                                  (440, 460), self.screen)
        self.apply = ClassicButton(_("Apply"), 90, 30,
                                   (345, 460), self.screen)
        self.choose_loc = TextLabel(_("Choose the language"),
                                    500, 30,
                                    (0, 30), self.screen, font=30)
        self.en = TextLabel("English", 110, 30,
                            (x + size + 10, y), self.screen, font=30)
        self.ru = TextLabel("Русский", 110, 30,
                            (x + size + 10, y + size + shift),
                            self.screen, font=30)
        self.choose_diff = TextLabel(_("Choose the number of "
                                       "notes for each game"),
                                     500, 30,
                                     (0, 190), self.screen, font=30)
        self.game1_label = TextLabel(_("Notes on stave:"),
                                     250, 30,
                                     (0, 250), self.screen, font=30)
        self.decrease1 = ClassicButton("-",
                                       30, 30, (250, 250), self.screen)
        self.notes1_label = TextLabel(f"{self.notes1}",
                                      30, 30,
                                      (280, 250), self.screen, font=30)
        self.increase1 = ClassicButton("+",
                                       30, 30, (310, 250), self.screen)
        self.game2_label = TextLabel(_("Notes by ear:"),
                                     250, 30,
                                     (0, 310), self.screen, font=30)
        self.decrease2 = ClassicButton("-",
                                       30, 30, (250, 310), self.screen)
        self.notes2_label = TextLabel(f"{self.notes2}",
                                      30, 30,
                                      (280, 310), self.screen, font=30)
        self.increase2 = ClassicButton("+",
                                       30, 30, (310, 310), self.screen)

    def draw(self):
        """Call to draw the settings screen."""
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
        self.notes1_label = TextLabel(f"{self.notes1}",
                                      30, 30, (280, 250),
                                      self.screen, font=30)
        self.notes1_label.draw()
        if self.decrease2.draw():
            if self.notes2 > 1:
                self.notes2 -= 1
        if self.increase2.draw():
            self.notes2 += 1
        self.notes2_label = TextLabel(f"{self.notes2}",
                                      30, 30, (280, 310),
                                      self.screen, font=30)
        self.notes2_label.draw()
        back = self.back.draw()
        apply = self.apply.draw()
        self.next = self.switch(back, apply)
        pygame.display.update()

    def update(self):
        """Call to update the settings screen."""
        return self.next

    def switch(self, back, apply):
        """Call to switch the screen."""
        if back:
            return MenuScreen()
        if apply:
            if self.check_loc.which_checked() == 1:
                Settings.set_localization("en")
            else:
                Settings.set_localization("ru")
            Settings.set_notes_on_stave(self.notes1)
            Settings.set_notes_by_ear(self.notes2)
            return MenuScreen()
        return self


class StatsScreen:
    """Class represents the screen of the statistics."""

    NEXT_BTN = os.path.join(os.path.dirname(__file__), "..", "assets", "next.png")
    PREV_BTN = os.path.join(os.path.dirname(__file__), "..", "assets", "prev.png")

    def __init__(self):
        """Initialise function for stats screen."""
        self.offset = 0
        self.limit = 10
        self.screen = pygame.display.get_surface()
        self.stats = StatsRepository()
        data = self.stats.get_games(self.offset, self.limit)
        self.games_list = list(
            ClassicButton(f"{data[i][1]}        "
                          f"{data[i][2]}/{data[i][3]}        "
                          f"{data[i][4]}", 250, 30,
                          (125, 100+i*28), self.screen,
                          clickable=False, border=0) for i in range(len(data))
        )
        self.next = self
        self.current_page = 1
        self.name = TextLabel(_("Games History"), 200, 30,
                              (150, 60), self.screen)
        self.back = ClassicButton(_("Back"), 50, 30,
                                  (440, 460), self.screen)
        self.total_pages = max(1, (self.stats.number_of_games() + self.limit
                                   - 1) // self.limit)
        self.previous_btn = ImageButton(30, 30, (115, 420),
                                        self.screen, self.PREV_BTN,
                                        clickable=False)
        if self.total_pages == 1:
            self.next_btn = ImageButton(30, 30, (355, 420),
                                        self.screen, self.NEXT_BTN,
                                        clickable=False)
        else:
            self.next_btn = ImageButton(30, 30,
                                        (355, 420), self.screen, self.NEXT_BTN)
        self.pages_label = TextLabel(_("Page {}/{}").format(self.current_page,
                                                            self.total_pages),
                                     90, 30, (205, 420),
                                     self.screen, 30)

    def draw(self):
        """Call to draw the stats screen."""
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
        """Call to switch to the next page."""
        self.offset += self.limit
        self.current_page += 1
        if self.current_page == 2:
            self.previous_btn = ImageButton(30, 30, (175, 420),
                                            self.screen, self.PREV_BTN)
        if self.current_page == self.total_pages:
            self.next_btn = ImageButton(30, 30, (295, 420),
                                        self.screen, self.NEXT_BTN,
                                        clickable=False)
        data = self.stats.get_games(self.offset, self.limit)
        self.games_list = list(
            ClassicButton(f"{data[i][1]}        "
                          f"{data[i][2]}/{data[i][3]}        "
                          f"{data[i][4]}", 250, 30,
                          (125, 100+i*28), self.screen,
                          clickable=False, border=0) for i in range(len(data))
        )
        self.pages_label = TextLabel(_("Page {}/{}").format(self.current_page,
                                                            self.total_pages),
                                     90, 30, (205, 420),
                                     self.screen, 30)

    def previous_page(self):
        """Call to switch to the previous page."""
        self.offset -= self.limit
        self.current_page -= 1
        if self.current_page == 1:
            self.previous_btn = ImageButton(30, 30,
                                            (175, 420),
                                            self.screen, self.PREV_BTN,
                                            clickable=False)
        if self.current_page == self.total_pages - 1:
            self.next_btn = ImageButton(30, 30,
                                        (295, 420), self.screen, self.NEXT_BTN)
        data = self.stats.get_games(self.offset, self.limit)
        self.games_list = list(
            ClassicButton(f"{data[i][1]}        "
                          f"{data[i][2]}/{data[i][3]}        "
                          f"{data[i][4]}", 250, 30,
                          (125, 100+i*28), self.screen,
                          clickable=False, border=0) for i in range(len(data))
        )
        self.pages_label = TextLabel(_("Page {}/{}").format(self.current_page,
                                                            self.total_pages),
                                     90, 30, (205, 420),
                                     self.screen, 30)

    def update(self):
        """Call to update the stats screen."""
        return self.next

    def switch(self, back):
        """Call to switch the screen."""
        if back:
            return MenuScreen()
        return self
