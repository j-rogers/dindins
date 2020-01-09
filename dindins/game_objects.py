"""Game Objects

This file contains objects used within the DinDins game such as walls and items.

Author: Josh Rogers
"""

import pygame

from dindins.settings import *


class Wall(pygame.Surface):
    def __init__(self, pos, width, height, colour=RED):
        super().__init__((width, height))
        self.rect = self.get_rect()
        self.rect.center = pos

        self.colour = colour

    def render(self):
        self.fill(self.colour)