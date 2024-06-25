import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 240, 100)
BLUE = (0, 100, 200)
DARK_BLUE = (0, 50, 255)
GRAY = (128, 128, 128)
BORDER = (0, 100, 100)


class ClassicButton:
    """Class represents the touch button"""

    TEXT_INTERVAL = 16

    def __init__(self, text, width, height, pos, screen, border=6, clickable=True):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = BORDER
        self.borders = border
        self.pressed = False
        self.frame = 2
        self.screen = screen
        self.clickable = clickable
        self.text_surf, self.text_rect = list(), list()
        self.text = text.split("\n")
        begin = -((len(self.text)//2)*self.TEXT_INTERVAL - ((len(self.text)+1)%2) * self.TEXT_INTERVAL//2)
        for i, line in enumerate(self.text):
            self.text_surf.append(m := pygame.font.Font(None, 20).render(line, True, '#000000'))
            self.text_rect.append(m.get_rect(centerx=self.top_rect.centerx, centery=self.top_rect.centery+begin))
            begin += self.TEXT_INTERVAL

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, self.frame, border_radius=self.borders)
        for surf, rect in zip(self.text_surf, self.text_rect):
            self.screen.blit(surf, rect)
        if self.covered():
            return True
        return False
    
    def covered(self):
        """Returns True if the button was pressed, False otherwise"""
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True

            if self.pressed and self.clickable:
                self.top_color = DARK_BLUE
            else:
                self.top_color = BLUE
            self.frame = 0
        else:
            self.pressed = False
            self.top_color = BORDER
            self.frame = 2
        return False


class SwitchButton:
    """Class represents the switch button"""

    def __init__(self, width, height, pos, screen, pic1=None, pic2=None):
        self.border_rect = pygame.Rect(*pos, width, height)
        self.inside_rect = pygame.Rect(*pos, width, height)
        self.switch_rect = pygame.Rect(pos[0]+1, pos[1]+1, width/2-1, height-2)
        self.pictures = {
            True: pygame.transform.scale(pygame.image.load(pic1), (width/2-1, height-2)) if pic1 else None,
            False: pygame.transform.scale(pygame.image.load(pic2), (width/2-1, height-2)) if pic2 else None
        }
        self.positions = {
            True: (pos[0]+1, pos[1]+1),
            False: (pos[0]+width/2, pos[1]+1)
        }
        self.pos = pos
        self.mode = True
        self.pressed = False
        self.last_press = pygame.time.get_ticks()
        self.width = width
        self.height = height
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, GRAY, self.inside_rect)
        pygame.draw.rect(self.screen, BORDER, self.border_rect, 2)
        pygame.draw.rect(self.screen, BLACK, self.switch_rect)
        if pic := self.pictures[self.mode]:
            self.screen.blit(pic, self.positions[not self.mode])
        if self.covered():
            if (m := pygame.time.get_ticks()) >= self.last_press + 500:
                self.last_press = m
                self.switch()
                return True
        return False

    def covered(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.border_rect.collidepoint(mouse_pos):
            clicked = pygame.mouse.get_pressed()[0]
            if clicked:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True
        return False

    def switch(self):
        if self.mode:
            self.switch_rect.update(self.pos[0]+self.width/2, self.pos[1]+1, self.width/2-1, self.height-2)
            self.mode = False
        else:
            self.switch_rect.update(self.pos[0]+1, self.pos[1]+1, self.width/2-1, self.height-2)
            self.mode = True


class ScoreLabel:
    """Class represents the score label"""
    
    def __init__(self, width, height, pos, screen, maxscore):
        self.score = 0
        self.maxscore = maxscore
        self.rect = pygame.Rect(*pos, width, height)
        self.text = pygame.font.Font(None, 20).render(f"{self.score}/{self.maxscore}", True, "#000000")
        self.text_rect = self.text.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        self.screen = screen

    def draw(self):
        self.text = pygame.font.Font(None, 20).render(f"{self.score}/{self.maxscore}", True, "#000000")
        self.text_rect = self.text.get_rect(centerx=self.rect.centerx, centery=self.rect.centery)
        pygame.draw.rect(self.screen, BLACK, self.rect, 2, border_radius=6)
        self.screen.blit(self.text, self.text_rect)

    def update(self):
        self.score += 1
    
class TextLabel:
    """Class represents the text label"""

    TEXT_INTERVAL = 16

    def __init__(self, text, width, height, pos, screen, font=20, **kwargs):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = GREEN
        self.pressed = False
        self.screen = screen
        self.text_surf, self.text_rect = list(), list()
        self.text = text.split("\n")
        begin = -((len(self.text)//2)*self.TEXT_INTERVAL - ((len(self.text)+1)%2) * self.TEXT_INTERVAL//2)
        for i, line in enumerate(self.text):
            fnt = pygame.font.Font(None, font)
            fnt.bold = kwargs.get("bold", False)
            fnt.italic = kwargs.get("italic", False)
            self.text_surf.append(m := fnt.render(line, True, '#000000'))
            self.text_rect.append(m.get_rect(centerx=self.top_rect.centerx, centery=self.top_rect.centery+begin))
            begin += self.TEXT_INTERVAL
    
    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect)
        for surf, rect in zip(self.text_surf, self.text_rect):
            self.screen.blit(surf, rect)


class ImageButton:
    """Class represents the image button"""

    def __init__(self, width, height, pos, screen, img_path, border=6, clickable=True):
        self.screen = screen
        self.width, self.height = width, height
        self.pos = pos
        self.border = border
        self.frame = 2
        self.top_color = BORDER
        self.pressed = False
        self.clickable = clickable
        self.top_rect = pygame.Rect(pos, (width, height))
        self.image = pygame.transform.scale(pygame.image.load(img_path), (width, height))

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, self.frame, border_radius=self.border)
        self.screen.blit(self.image, self.pos)
        return self.covered()

    def covered(self):
        """Returns True if the button was pressed, False otherwise"""
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True

            if self.pressed and self.clickable:
                self.top_color = DARK_BLUE
            else:
                self.top_color = BLUE
            self.frame = 0
        else:
            self.pressed = False
            self.top_color = BORDER
            self.frame = 2
        return False


class CheckBoxPair:
    """Class represents the pair of check boxes"""

    def __init__(self, surface, x, y, color=(230, 230, 230), outline_color=(0, 0, 0),
                 check_color=(0, 0, 0), size=30, shift=30, first_check=1):
        self.collision1 = pygame.Rect((x, y), (size, size))
        self.collision2 = pygame.Rect((x, y + size + shift), (size, size))
        self.surface = surface
        self.x = x
        self.y = y
        self.shift = shift
        self.color = color
        self.oc = outline_color
        self.cc = check_color
        self.size = size
        self.checkbox1_obj = pygame.Rect(self.x, self.y, size, size)
        self.checkbox1_outline = self.checkbox1_obj.copy()
        self.checkbox2_obj = pygame.Rect(self.x, self.y + size + shift, size, size)
        self.checkbox2_outline = self.checkbox2_obj.copy()
        if first_check == 1:
            self.checked1 = True
            self.checked2 = False
        else:
            self.checked1 = False
            self.checked2 = True

    def draw(self):
        self.update()
        if self.checked1:
            pygame.draw.rect(self.surface, self.color, self.checkbox1_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox1_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + self.size // 2, self.y + self.size // 2),
                           int(self.size * 1 / 3))

            pygame.draw.rect(self.surface, self.color, self.checkbox2_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox2_outline, 1)

        else:
            pygame.draw.rect(self.surface, self.color, self.checkbox1_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox1_outline, 1)

            pygame.draw.rect(self.surface, self.color, self.checkbox2_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox2_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + self.size // 2, self.y + (self.size + self.shift) + self.size // 2),
                               int(self.size * 1 / 3))

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.collision1.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.checked2:
                self.checked1 = not self.checked1
                self.checked2 = not self.checked2
        elif self.collision2.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0] and self.checked1:
                self.checked1 = not self.checked1
                self.checked2 = not self.checked2

    def which_checked(self):
        """Returns 1 if the first check box is checked, 2 if the second check box is checked"""

        if self.checked1:
            return 1
        else:
            return 2