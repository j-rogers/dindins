"""Game Objects

This file contains functional objects used within DinDins. A functional object is an object that requires to be
extended beyond the BaseObject class, such as an interactable object. Decorations and regular objects that have no
functionality can simply be created from the BaseObject class.

Author: Josh Rogers
"""

import pygame

from dindins.settings import *
from dindins.gui import *


class ObjectsGroup(pygame.sprite.Group):
    """Group for game objects

    This class is an extension of pygame.sprite.Group to provide a Group for game objects. This implementation inlcudes
    two key extentions; the colliders() and interactables() methods. These methods return a subset Group of objects that
    have the collide and interactable properties. These can be used in the main game loop to easily detect collisions
    and objects for interactions.
    """
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

    def get(self, objectname):
        for object in self.sprites():
            if object.name == objectname:
                return object

        return None


class BaseObject(pygame.sprite.Sprite):
    """Base object

    This class provides a base for in game objects, and is treated as a pygame.sprite.Sprite. As they are sprites, each
    object requires an image property. Each object has the option to be a collider or interactable, through the collide
    and interactable properties, respectively. If interactable is set, then the interact method MUST be implemented.

    Attributes:
        image: Image surface of the sprite
        rect: pygame.Rect of the image
        name: Unique name of the object to identify it and retrieve it in a group
        collide: Bool indicating if collision should be checked with this object (defaults to False)
        interactable: Bool indicating if this object can be interacted with (defaults to False)
    """
    def __init__(self, pos, image, name, collide=False, interactable=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.name = name

        self.collide = collide
        self.interactable = interactable

    def interact(self):
        """Triggered when player interacts with the object

        To be implemented in objects that have the interactable property set. This method should return any GUI objects
        (e.g. Dialogue boxes) to be rendered.
        """
        raise NotImplementedError


class Wall(BaseObject):
    """Wall

    This is a simple wall that is used for barriers around the map.  The image is just a jpg of a solid colour so it can
    be transformed without stretching any textures. As the wall acts as a barrier, the collide property is set.
    """
    def __init__(self, pos, width, height, name):
        """Init

        Args:
            pos: Tuple in form (x, y) providing coordinates of where to place the wall
            width: Width of the wall
            height: Height of the wall
        """
        image = pygame.image.load(f'{ASSETS}/terrain/wall.png')
        image = pygame.transform.scale(image, (width, height))
        super().__init__(pos, image, name, collide=True)


class Door(BaseObject):
    """Door

    Doors are interactable objects.
    """
    def __init__(self, pos, width, height, message, name):
        """Init

        Args:
            pos: Coordinates of where to place the door
            width: Width of the door
            height: Height of the door
            message: Message to give to the user when door is used
        """
        image = pygame.image.load(f'{ASSETS}/terrain/wall.png')
        image = pygame.transform.scale(image, (width, height))
        super().__init__(pos, image, name, interactable=True)

        self.message = message

    def interact(self):
        """Interact

        Gives the user a dialogue box with the provided message.

        Returns:
            Dialogue box
        """
        box = DialogueBox(self.message, (WIDTH / 2, HEIGHT * .8))
        return box


class Floor:
    def __init__(self, pos, width, height, name, type='floorboard'):
        self.sprites = []

        x = 0
        y = 0

        images = {
            'tile': pygame.image.load(f'{ASSETS}/terrain/tile.png'),
            'floorboard': pygame.image.load(f'{ASSETS}/terrain/floorboard.png'),
            'carpet': pygame.image.load(f'{ASSETS}/terrain/carpet.png'),
        }

        image = images[type]

        done = False
        while not done:
            if x > width:
                x = 0
                y += 32

            if y > height:
                done = True
                continue

            self.sprites.append(BaseObject((pos[0] - x, pos[1] - y), image, name))
            x += 32


class Bed(BaseObject):
    def __init__(self, pos, name, orientation='horizontal'):
        image = pygame.image.load(f'{ASSETS}/objects/bed.png')
        if orientation == 'horizontal':
            image = pygame.transform.rotate(image, 90)
        super().__init__(pos, image, name, collide=True, interactable=True)

    def interact(self):
        pygame.event.post(pygame.event.Event(HIDE, {'object': self, 'move': False}))
