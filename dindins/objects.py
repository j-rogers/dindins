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

    def triggerables(self):
        triggerables = []
        for object in self.sprites():
            if object.triggerable:
                triggerables.append(object)

        return pygame.sprite.Group(triggerables)

    def get(self, objectname):
        for object in self.sprites():
            if object.name == objectname:
                return object

        return None


class BaseObject(pygame.sprite.Sprite):
    """Base object

    This class provides a base for in game objects, and is treated as a pygame.sprite.Sprite. As they are sprites, each
    object requires an image property. Each object can set a specific property to enable certain functionality. If a
    set property has a corresponding method, then that method MUST be implemented.

    Available Properties:
        interactable: An interactable object is an object that performs the interact() method when the player presses
            space bar near it. MUST IMPLEMENT interact() METHOD.
        boundingbox: If set, collision will be detected on the object. The player will not be able to move through the
            object.
        triggerable: A trigger object is an object that performs the trigger() method when the player walks into it (as
            opposed to pressing the space bar as with the interactable property). MUST IMPLEMENT trigger() METHOD.

    Attributes:
        image: Image surface of the sprite
        rect: pygame.Rect of the image
        name: Unique name of the object to identify it and retrieve it in a group
        interactable: Bool indicating if this object can be interacted with (defaults to False)
        boundingbox: pygame.Rect used to detect collision
    """
    def __init__(self, pos, image, name, interactable=False, boundingbox=None, triggerable=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.name = name

        self.interactable = interactable
        self.triggerable = triggerable

        if boundingbox:
            if boundingbox == 'image':
                self.boundingbox = self.rect.copy()
            else:
                if len(boundingbox) > 2:
                    width = boundingbox[2] + boundingbox[0]
                    height = boundingbox[1] + boundingbox[3]
                    self.boundingbox = pygame.Rect(0, 0, width, height)
                    self.boundingbox.left = pos[0] + boundingbox[0]
                    self.boundingbox.top = pos[1] + boundingbox[1]
                    self.boundingbox.right = pos[0] + boundingbox[2]
                    self.boundingbox.bottom = pos[1] + boundingbox[3]
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

    def trigger(self):
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


class Animated(BaseObject):
    def __init__(self, pos, image, name, interactable=False, boundingbox=None, triggerable=False):
        """Initialises the character"""
        super().__init__(pos, image, name, interactable=interactable, boundingbox=boundingbox, triggerable=triggerable)

        # Animation variables
        self.direction = 'down'
        self.index = 0
        self.ticker = 0
        self.rate = 2
        self.pause = False

        # Animation images
        self.idle = {}
        self.walk = {}

    def _playanimation(self, animation):
        """Plays the specified animation

        The ticker increments with every frame, so we perform a modulus using the FPS and rate to calculate when a new
        animation image should be displayed.

        Args:
            animation: List of images that create the animation
            rate: Rate that frames should be shown per second
        """
        if self.ticker % (FPS / self.rate) == 0:
            # Reset the index if reached the end of the animation
            self.index = 0 if self.index == len(animation) else self.index

            self.image = animation[self.index]

            # Increase index
            self.index += 1

        self.ticker += 1

    def update(self):
        """Update sprite

        This method handles all the live updates for the sprite. This includes changing animations for current key
        presses.
        """
        raise NotImplementedError


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


class SpawnTrigger(BaseObject):
    def __init__(self, pos, image, name, *spawn, boundingbox=None):
        super().__init__(pos, image, name, boundingbox=boundingbox, triggerable=True)
        self.spawn = spawn

    def trigger(self):
        self.remove(self.groups())
        pygame.event.post(pygame.event.Event(RENDER, {'objects': [object for object in self.spawn]}))


class Bowls(DialogueBoxObject):
    def __init__(self, objectives):
        super().__init__((595, -260), pygame.image.load(f'{ASSETS}/objects/bowls.png'), 'Yummy food!', 'bowls', boundingbox=(1, 24, 8, 24))
        self.objectives = objectives

    def interact(self):
        if self.objectives[0] == 'eat_food':
            self.message = 'What was that?                       ...                  I should go hide under the bed!'
            super().interact()
            pygame.event.post(pygame.event.Event(OBJECTIVE, {'objective': self.objectives[0]}))
        elif self.objectives[0] == 'hide_under_bed':
            # PLAY BANG SOUND
            self.message = 'I need to hide under the bed!'
            super().interact()
        else:
            self.message = 'Yummy food, but no time for that now!'
            super().interact()


class Bed(HideObject):
    def __init__(self, objectives):
        super().__init__((395, 210), pygame.image.load(f'{ASSETS}/objects/bed.png'), 'bed', boundingbox=(30, 38, 18, 15))
        self.objectives = objectives

    def interact(self):
        super().interact()
        if self.objectives[0] == 'hide_under_bed':
            box = DialogueBox('I think the coast is clear... I can go back to eating my breakfast.', (WIDTH / 2, HEIGHT * .8))
            pygame.event.post(pygame.event.Event(RENDER, {'objects': [box]}))
            pygame.event.post(pygame.event.Event(OBJECTIVE, {'objective': self.objectives[0]}))


def tile(pos, width, height, name, boundingbox=None):
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
