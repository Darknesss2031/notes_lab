import unittest
import pygame
from src.tools import CheckBoxPair, SwitchButton
from src.screens import MenuScreen, GameMenuScreen, SettingsScreen, NotesOnStaveScreen, GameOverScreen


class TestCheckBoxPair(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.target = CheckBoxPair(pygame.display.get_surface(), 10, 10, first_check=1)
        return super().setUpClass()

    def test_1(self):
        output = self.target.which_checked()
        self.assertEqual(output, 1)

    def test_2(self):
        self.target.switch_checked()
        output = self.target.which_checked()
        self.assertEqual(output, 2)


class TestSwitchButton(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.target = SwitchButton(10, 10, (10, 10), pygame.display.get_surface())
        return super().setUpClass()

    def test_3(self):
        output = self.target.mode
        self.assertEqual(output, True)

    def test_4(self):
        self.target.switch()
        output = self.target.mode
        self.assertEqual(output, False)


class TestMenuScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.target = MenuScreen()
        return super().setUpClass()

    def test_5(self):
        output = self.target.switch(True, False, False)
        self.assertEqual(isinstance(output, GameMenuScreen), True)

    def test_6(self):
        output = self.target.switch(False, False, True)
        self.assertEqual(isinstance(output, SettingsScreen), True)


class TestSettingsScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.target = SettingsScreen()
        return super().setUpClass()

    def test_7(self):
        output = self.target.switch(False, True)
        self.assertEqual(isinstance(output, MenuScreen), True)

    def test_8(self):
        output = self.target.switch(True, False)
        self.assertEqual(isinstance(output, MenuScreen), True)


class TestNotesOnStaveScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.target = NotesOnStaveScreen()
        return super().setUpClass()

    def test_9(self):
        output = self.target.switch(False, True)
        self.assertEqual(isinstance(output, GameOverScreen), True)

    def test_10(self):
        output = self.target.switch(True, False)
        self.assertEqual(isinstance(output, GameMenuScreen), True)