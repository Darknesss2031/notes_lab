from tools import ClassicButton, ScoreLabel, ImageButton, TextLabel
from threading import Thread
import os
import random
from itertools import product
import pygame
from stats import StatsRepository
from datetime import datetime
import gettext


RETRY_ICON = os.path.join(os.getcwd(), "assets", "reload.png")
NEXT_ICON = os.path.join(os.getcwd(), "assets", "forward-button.png")
notes_for_gen = list(chr(ord('a')+i)+"1" for i in range(7))
notes_for_gen.append("c2")

LOCALES = {
    "ru": gettext.translation("loc", f"{os.getcwd()}/loc", ["ru"], fallback=False),
    "en": gettext.NullTranslations()
}
current_locale = "en"


def _(text):
    return LOCALES[current_locale].gettext(text)


class Note:
    """Class representing note sound"""

    def __init__(self, name):
        self.name = name
        self.sound = pygame.mixer.Sound(os.path.join(os.getcwd(), "assets", name+".mp3"))

    def play(self):
        self.sound.play()


class GameProcess:
    """Class for main gaming process"""

    STOP = False

    def __init__(self, screen, maxscore, loc="en"):
        self.current_note = None
        global current_locale
        current_locale = loc
        self.screen = screen
        self.correct, self.incorrect = 0, 0
        self.maxscore = maxscore
        self.generated = 0
        self.score = ScoreLabel(50, 20, (225, 235), self.screen, self.maxscore)
        self.answer = TextLabel(_("Guess the note"), 100, 50, (200, 100), screen, 70)
        self.retry_btn = ImageButton(50, 50, (195, 180), screen, RETRY_ICON)
        self.next_btn = ImageButton(50, 50, (255, 180), screen, NEXT_ICON)
        self.stats = StatsRepository()

    def start_game(self):
        self.next_note()
        self.guessed = False
    
    def end_game(self):
        self.STOP = True
        self.stats.add_game("Notes by ear", self.correct, self.maxscore, datetime.now().strftime("%d-%m-%Y"))

    def next_note(self):
        if self.generated == self.maxscore:
            self.STOP = True
            return
        self.guessed = False
        self.generated += 1
        self.current_note = Note(random.choice(notes_for_gen))
        self.current_note.play()
        self.answer = TextLabel(_("Guess the note"), 100, 50, (200, 100), self.screen, 70)

    def play_note(self):
        self.current_note.play()

    def process_key(self, key):
        if self.current_note.name[0] == key[0]:
            if not self.guessed:
                self.correct += 1
                self.score.update()
            self.answer = TextLabel(_("Correct! This was {}").format(self.current_note.name), 100, 50, (200, 100), self.screen, 40)
        else:
            if not self.guessed:
                self.incorrect += 1
            self.answer = TextLabel(_("Wrong note, try again"), 100, 50, (200, 100), self.screen, 40)
        self.guessed = True