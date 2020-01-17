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
        interactable: Bool indicating if this object can be interacted with (defaults to False)
        boundingbox: pygame.Rect used to detect collision
    """
    def __init__(self, pos, image, name, interactable=False, boundingbox=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.name = name

        self.interactable = interactable

        if boundingbox:
            if boundingbox == 'image':
                self.boundingbox = self.rect.copy()
            else:
                self.boundingbox = pygame.Rect((self.rect.left, self.rect.top), boundingbox)
                self.boundingbox.center = pos
        else:
            self.boundingbox = boundingbox

    def interact(self):
        """Triggered when player interacts with the object

        To be implemented in objects that have the interactable property set.
        """
        raise NotImplementedError

    def move(self, x, y):
        """Shifts the object

        Shifts the object by x and y. Additionally moves the bounding box if one is present.

        Args:
            x: Pixel value to move the object horizontally
            y: Pixel value to move the object vertically
        """
        self.rect.move_ip(x, y)
        if self.boundingbox:
            self.boundingbox.move_ip(x, y)


class DialogueBoxObject(BaseObject):
    """An interactable tile that creates a dialogue box

    Doors are interactable objects that present the player with a dialogue box.
    """
    def __init__(self, pos, image, message, name, boundingbox=None):
        """Init

        Args:
            pos: Coordinates of where to place the door
            width: Width of the door
            height: Height of the door
            message: Message to give to the user when door is used
        """
        super().__init__(pos, image, name, interactable=True, boundingbox=boundingbox)
        self.message = message

    def interact(self):
        """Interact

        Gives the user a dialogue box with the provided message.

        Returns:
            Dialogue box
        """
        box = DialogueBox(self.message, (WIDTH / 2, HEIGHT * .8))
        pygame.event.post(pygame.event.Event(RENDER, {'objects': [box]}))


class HideObject(BaseObject):
    """Object that the player can hide under

    This object is an interactable object that allows the player the hide under it. This is achieved by posting the HIDE,
    allowing the game screen to handle the rest.
    """
    def __init__(self, pos, image, name, boundingbox=None):
        """Init

        Args:
            pos: Position of the center of the object
            image: pygame.Surface of the object
            name: Name of the object
            boundingbox: Bounding box of the object. If none is set then it will default to the size of the image.
        """
        box = (image.get_width(), image.get_height()) if not boundingbox else boundingbox
        super().__init__(pos, image, name, boundingbox=box, interactable=True)

    def interact(self):
        """Posts the HIDE event"""
        pygame.event.post(pygame.event.Event(HIDE, {'object': self, 'move': False}))


def tile(pos, width, height, name, collide=True):
    """Creates a tile of a solid colour

    This is a simple function that creates a tile of given width and height of a solid colour.

    Args:
        pos: Position of the center of the tile
        width: Width of the tile in pixels
        height: Height of the tile in pixels
        name: Name of the tile
        collide: Determines if the tile should have collision (Defaults to true)
    """
    surface = pygame.Surface((width, height))
    surface.fill(GREY)
    boundingbox = (width, height) if collide else None
    return BaseObject(pos, surface, name, boundingbox=boundingbox)


def tileset(pos, width, height, name, type='floorboard'):
    """Creates a list of tiles in a given area

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
