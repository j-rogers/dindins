"""Game Objects

This file contains objects used within the DinDins game such as walls and items.

Author: Josh Rogers
"""

import pygame

from dindins.settings import *


class ObjectsGroup:
    def __init__(self, *objects):
        self.objects = []
        self.colliders = []
        self.interactables = []

        self.add(objects)

    def add(self, *objects):
        if not objects[0]:
            return None
        for object in objects:
            self.objects.append(object)

            if object.collide:
                self.colliders.append(object)
            if object.interactable:
                self.interactables.append(object)

class SurfaceObject(pygame.Surface):
    def __init__(self, pos, width, height, colour, collide=False, interactable=False):
        super().__init__((width, height))
        self.rect = self.get_rect()
        self.rect.center = pos

        self.colour = colour

        self.collide = collide
        self.interactable = interactable

    def interact(self):
        pass

    def render(self):
        self.fill(self.colour)


class Wall(SurfaceObject):
    def __init__(self, pos, width, height, colour=RED):
        super().__init__(pos, width, height, colour, collide=True)


class Door(SurfaceObject):
    def __init__(self, pos, width, height, message, colour=GREEN):
        super().__init__(pos, width, height, colour, interactable=True)
        self.message = message

    def interact(self):
        print('door')