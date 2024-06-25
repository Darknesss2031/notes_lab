"""This file contains notes on stave game logic"""
import pygame
import os
from queue import Queue
from time import sleep
from piano import Piano
from tools import BLACK, GREEN
import random
from threading import Thread
from tools import ClassicButton, ScoreLabel
from stats import StatsRepository
from datetime import datetime


notes_for_gen = ["b2", "a2", "g2", "f2", "e2", "d2", "c2", "b1", "a1", "g1", "f1", "e1", "d1", "c1"]
notes_bass = ["d0", "c0", "b1", "a1", "g1", "f1", "e1", "d1", "c1", "b2", "a2", "g2", "f2", "e2"]
notes_height = {}


class Line:
    """Class representing line on the stave"""

    def __init__(self, color, pos, width, screen):
        self.pos = pos.copy()
        self.width = width
        self.color = color
        self.screen = screen

    def draw(self):
        pygame.draw.line(self.screen, self.color, self.pos, (self.pos[0]+self.width, self.pos[1]), 2)

    def move(self, delta):
        self.pos = (self.pos[0]-delta, self.pos[1])


class Note:
    """Class representing note symbols"""

    def __init__(self, x, y, screen, name, icon="note.png", extra=False, underline=False):
        self.pos = (x, y-45)
        self.screen = screen
        self.name = name
        self.underline = Line(BLACK, [x+10, y+12], 20, screen) if underline else None
        self.extra = Line(BLACK, [x+10, y], 20, screen) if extra else None
        self.icon = pygame.image.load(os.path.join(os.getcwd(), "assets", icon))
        self.icon = pygame.transform.scale(self.icon, (50, 50))

    def draw(self):
        if self.extra:
            self.extra.draw()
        if self.underline:
            self.underline.draw()
        self.screen.blit(self.icon, self.pos)
    
    def move(self, delta):
        m = list(self.pos)
        self.pos = (m[0]-delta, m[1])
        if self.extra:
            self.extra.move(delta)
        if self.underline:
            self.underline.move(delta)


class Stave:
    """Class representing the stave"""

    DISTANCE = 12
    SPEED = 2
    ADDING = 65

    def __init__(self, width, pos, screen):
        self.screen = screen
        self.width = width
        self.pos = pos
        self.lines = []
        self.notes = []
        self.key = pygame.image.load(os.path.join(os.getcwd(), "assets", "key.png"))
        self.key = pygame.transform.scale(self.key, (100, 100))
        colors = [BLACK, GREEN]
        off_pos = list(self.pos)
        off_pos[1] -= self.DISTANCE*3
        for i in range(3):
            notes_height[notes_for_gen[i]] = off_pos[1]
            off_pos[1] += self.DISTANCE
        for i in range(3, 12):
            self.lines.append(Line(colors[(i+1)%2], off_pos, self.width, self.screen))
            notes_height[notes_for_gen[i]] = off_pos[1]
            off_pos[1] += self.DISTANCE
        for i in range(12, 14):
            notes_height[notes_for_gen[i]] = off_pos[1]
            off_pos[1] += self.DISTANCE

    def draw(self):
        for line in self.lines:
            line.draw()
        pos = list(self.lines[6].pos)
        self.screen.blit(self.key, (pos[0]-25, pos[1]-self.ADDING))
        for note in self.notes:
            note.draw()
        
    def move(self):
        if not len(self.notes) == 0 and self.notes[0].pos[0] <= self.pos[0]+50:
            self.notes.pop(0)
        for note in self.notes:
            note.move(self.SPEED)
    
    def change_key(self, path):
        if self.ADDING == 65:
            self.ADDING += 2*self.DISTANCE-2
        else:
            self.ADDING -= 2*self.DISTANCE-2
        self.key = pygame.image.load(path)
        self.key = pygame.transform.scale(self.key, (100, 100))

    def set_speed(self, speed):
        self.SPEED = speed


class GameProcess:
    """Class for main gaming process"""

    STOP = False
    ACTIVE = False
    LAST_GEN = 0
    GAME_MODE = "TREB"
    KEY_PATH = {
        "TREB": os.path.join(os.getcwd(), "assets", "key.png"),
        "BASS": os.path.join(os.getcwd(), "assets", "bass.png")
    }


    def __init__(self, screen, maxscore=30, alter=False):
        self.screen = screen
        self.stave = Stave(400, (50, 80), screen)
        self.correct, self.incorrect = 0, 0
        self.maxscore = maxscore
        self.generated = 0
        self.ALTER = alter
        self.score = ScoreLabel(50, 20, (225, 235), self.screen, self.maxscore)
        self.stats = StatsRepository()

        def move(self):
            while True:
                sleep(0.1)
                self.LAST_GEN += 0.1
                if self.maxscore == self.correct+self.incorrect:
                    self.STOP = True
                    return
                if not self.ACTIVE:
                    continue
                if self.STOP:
                    return
                if self.LAST_GEN >= 3:
                    self.generate_note()
                    self.LAST_GEN = 0
                self.stave.move()
        
        self.ticker = Thread(target=move, args=(self,))
        self.ticker.start()

    def start_game(self):
        self.ACTIVE = True
        self.generate_note()

    def end_game(self):
        self.STOP = True
        self.ticker.join()
        self.stats.add_game("Notes on stave", self.correct, self.maxscore, datetime.now().strftime("%d-%m-%Y"))
    
    def choose_icon(self, name, alter, oct):
        return "note.png"
        if oct == 2 or oct == 1 and name == "b1":
            if alter:
                return "rev_alter.png"
            return "rev.png"
        if alter:
            return "alter.png"
        return "note.png"
    
    def generate_note(self):
        if self.generated == self.maxscore:
            return
        self.generated += 1
        name = random.choice(notes_for_gen)
        oct = name[-1]
        alter = random.choice([False, False, False, False])
        icon = self.choose_icon(name, alter, oct)
        name += ("#" if alter else "")
        underline = True if name.startswith("b2") else False
        extra = True if name.startswith("a2") or name.startswith("c1") else False
        note = Note(400, notes_height[name], self.screen, name, icon, extra, underline)
        self.stave.notes.append(note)

    def change_mode(self):
        if self.GAME_MODE == "TREB":
            self.GAME_MODE = "BASS"
            self.stave.change_key(self.KEY_PATH["BASS"])
        else:
            self.GAME_MODE = "TREB"
            self.stave.change_key(self.KEY_PATH["TREB"])

    def process_key(self, key):
        if len(self.stave.notes) == 0:
            return
        name = self.stave.notes[0].name
        if self.GAME_MODE == "BASS":
            name = notes_bass[notes_for_gen.index(name.rstrip('#'))] + ("#" if name.endswith("#") else "")
        if name[0]+name[2:] == key:
            self.correct += 1
            self.score.update()
        else:
            self.incorrect += 1
        
        self.stave.notes.pop(0)