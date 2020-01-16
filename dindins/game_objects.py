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
            if object.boundingbox:
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
    def __init__(self, pos, image, name, collide=False, interactable=False, boundingbox=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.name = name

        self.collide = collide
        self.interactable = interactable

        if boundingbox:
            self.boundingbox = pygame.Rect((self.rect.left, self.rect.top), boundingbox)
            self.boundingbox.center = pos
        else:
            self.boundingbox = boundingbox

    def interact(self):
        """Triggered when player interacts with the object

        To be implemented in objects that have the interactable property set. This method should return any GUI objects
        (e.g. Dialogue boxes) to be rendered.
        """
        raise NotImplementedError

    def move(self, x, y):
        self.rect.move_ip(x, y)
        if self.boundingbox:
            self.boundingbox.move_ip(x, y)


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
        super().__init__(pos, image, name, boundingbox=(width, height))


class Door(BaseObject):
    """Door

    Doors are interactable objects that present the player with a dialogue box.
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


class Bed(BaseObject):
    def __init__(self, pos, name, orientation='horizontal'):
        image = pygame.image.load(f'{ASSETS}/objects/bed.png')
        if orientation == 'horizontal':
            image = pygame.transform.rotate(image, 90)
        super().__init__(pos, image, name, boundingbox=(96, 64), interactable=True)

    def interact(self):
        pygame.event.post(pygame.event.Event(HIDE, {'object': self, 'move': False}))


class BoundingBox(BaseObject):
    def __init__(self, pos, width, height, name):
        image = pygame.image.load(f'{ASSETS}/terrain/transparent.png')
        image = pygame.transform.scale(image, (width, height))
        super().__init__(pos, image, name, boundingbox=(width, height))


def floor(pos, width, height, name, type='floorboard'):
    """Creates a list of tiles in a given area for flooring

    This method uses the given width and height to create a list of tiles that fit in the given area. The tiles are each
    32x32, and the width and height must be given in number of tiles.

    Args:
        pos: Tuple in the form (x, y) specifying the center of the area
        width: Width of the area in tiles
        height: Height of the area in tiles
        name: Name of the area
        type: Type of image to use for the sprites (defaults to floorboard) Possible options include tile, floorboard,
            and carpet.
    """


    # Get image to use
    images = {
        'tile': pygame.image.load(f'{ASSETS}/terrain/tile.png'),
        'floorboard': pygame.image.load(f'{ASSETS}/terrain/floorboard.png'),
        'carpet': pygame.image.load(f'{ASSETS}/terrain/carpet.png'),
    }
    image = images[type]

    # List of sprites
    sprites = []

    # Coordinates of current tile
    x = 0
    y = 0

    # Build list until all rows are filled
    while y <= height * 32:

        # Place sprite (relative to given pos) and increment x by 32
        sprites.append(BaseObject((pos[0] - x, pos[1] - y), image, name))
        x += 32

        # Go to next row if x exceeds width
        if x > width * 32:
            x = 0
            y += 32

    return sprites
