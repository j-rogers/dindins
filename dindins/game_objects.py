"""Game Objects

This file contains objects used within the DinDins game such as walls and items.

Author: Josh Rogers
"""

import pygame

from dindins.settings import *


class ObjectsGroup(pygame.sprite.Group):
    def __init__(self, *objects):
        super().__init__(objects)

    def colliders(self):
        colliders = []
        for object in self.sprites():
            if object.collide:
                colliders.append(object)

        return pygame.sprite.Group(colliders)

    def interactables(self):
        interactables = []
        for object in self.sprites():
            if object.interactable:
                interactables.append(object)

        return pygame.sprite.Group(interactables)


class BaseObject(pygame.sprite.Sprite):
    def __init__(self, pos, image, collide=False, interactable=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.collide = collide
        self.interactable = interactable

    def interact(self):
        pass


class Wall(BaseObject):
    def __init__(self, pos, width, height):
        image = pygame.image.load(f'{ASSETS}/terrain/wall.jpg')
        image = pygame.transform.scale(image, (width, height))
        super().__init__(pos, image, collide=True)


class Door(BaseObject):
    def __init__(self, pos, width, height, message):
        image = pygame.image.load(f'{ASSETS}/terrain/wall.jpg')
        image = pygame.transform.scale(image, (width, height))
        super().__init__(pos, image, interactable=True)

        self.message = message

    def interact(self):
        print('door')