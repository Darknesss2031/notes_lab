import pygame
from .tools import WHITE, BLACK, GRAY


class WhiteButton:
    """Class represents the white piano button"""

    def __init__(self, name, width, height, pos, screen, blacks):
        self.name = name
        self.blacks = blacks
        self.top_rect = pygame.Rect(pos, (width, height))
        self.frame = pygame.Rect(pos, (width, height))
        self.top_color = WHITE
        self.frame_color = BLACK
        self.pressed = False
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect)
        pygame.draw.rect(self.screen, self.frame_color, self.frame, 1)
        if self.covered():
            return True
        return False
    
    def covered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                if any((x.top_rect.colliderect(self.top_rect) and x.top_rect.collidepoint(mouse_pos) for x in self.blacks)):
                    self.top_color = WHITE
                    return False
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                self.top_color = WHITE
                return True

            if self.pressed:
                self.top_color = GRAY
            else:
                self.top_color = WHITE
        else:
            self.top_color = WHITE
        return False


class BlackButton:
    """Class represents the black piano button"""

    def __init__(self, name, width, height, pos, screen):
        self.name = name
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = BLACK
        self.pressed = False
        self.screen = screen
        self.frame = 0

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, self.frame)
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
                self.top_color = BLACK
                return True

            if self.pressed:
                self.top_color = GRAY
                self.frame = 0
            else:
                self.top_color = BLACK
        else:
            self.top_color = BLACK
            self.frame = 0
        return False


class Piano:
    """Class represents the piano"""

    START_POS_WHITE = 75
    START_POS_BLACK = START_POS_WHITE+40

    def __init__(self, screen):
        self.keys = []
        whites = ["c", "d", "e", "f", "g", "a", "b"]
        blacks = ["c#", "d#", "f#", "g#", "a#"]
        self.screen = screen
        self.black_keys = []

        start = self.START_POS_BLACK
        for i in range(5):
            self.keys.append(m := BlackButton(blacks[i], 20, 100, (start, 300), self.screen))
            self.black_keys.append(m)
            if i == 1:
                start += 50
            start += 50

        start = self.START_POS_WHITE
        for i in range(7):
            self.keys.append(WhiteButton(whites[i], 50, 150, (start, 300), self.screen, self.black_keys))
            start += 50
        self.pressed = None

    def draw(self):
        self.pressed = None
        for key in reversed(self.keys):
            if key.draw():
                self.pressed = key.name
        return self.pressed
