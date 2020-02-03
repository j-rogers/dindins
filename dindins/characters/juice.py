import pygame

from dindins.settings import *
from dindins.objects import Animated


class Juice(Animated):
    def __init__(self, pos):
        super().__init__(pos, pygame.image.load(f'{ASSETS}/juice/idle/juice_idle_down.png'), 'juice', triggerable=True)
        self.boundingbox = self.rect.copy()

        self.distance = 0
        self.flip = False

        self.idle = {
            'up': pygame.image.load(f'{ASSETS}/juice/idle/juice_idle_up.png'),
            'down': pygame.image.load(f'{ASSETS}/juice/idle/juice_idle_down.png'),
            'left': pygame.image.load(f'{ASSETS}/juice/idle/juice_idle_left.png'),
            'right': pygame.image.load(f'{ASSETS}/juice/idle/juice_idle_right.png')
        }

        self.walk = {
            'up': [
                pygame.image.load(f'{ASSETS}/juice/walk/up/juice_walk_up_1.png'),
                pygame.image.load(f'{ASSETS}/juice/walk/up/juice_walk_up_2.png')
            ],
            'down': [
                pygame.image.load(f'{ASSETS}/juice/walk/down/juice_walk_down_1.png'),
                pygame.image.load(f'{ASSETS}/juice/walk/down/juice_walk_down_2.png')
            ],
            'left': [
                pygame.image.load(f'{ASSETS}/juice/walk/left/juice_walk_left_1.png'),
                pygame.image.load(f'{ASSETS}/juice/walk/left/juice_walk_left_2.png')
            ],
            'right': [
                pygame.image.load(f'{ASSETS}/juice/walk/right/juice_walk_right_1.png'),
                pygame.image.load(f'{ASSETS}/juice/walk/right/juice_walk_right_2.png')
            ]
        }

    def trigger(self):
        pass

    def move(self, x, y):
        """Shifts the object by x and y

        Args:
            x: Pixel value to move the object horizontally
            y: Pixel value to move the object vertically
        """
        self.rect.move_ip(x, y)
        if self.boundingbox:
            self.boundingbox.move_ip(x, y)

    def update(self):
        if not self.pause:
            if not self.flip:
                self.move(0, 1)
                self._playanimation(self.walk['down'])
                self.distance += 1
                self.flip = True if self.distance == 800 else False
            elif self.flip:
                self.move(0, -1)
                self._playanimation(self.walk['up'])
                self.distance -= 1
                self.flip = False if self.distance == 0 else True
