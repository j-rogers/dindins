import pygame

from dindins.settings import *
from . import Character


class Juice(Character):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(f'{ASSETS}/juice/idle/juice_idle_down.png')
        self.rect = self.image.get_rect()
        self.rect.center = pos

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

    def update(self):
        pass
