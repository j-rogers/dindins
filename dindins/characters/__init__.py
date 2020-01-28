import pygame

from dindins.settings import *


class Character(pygame.sprite.Sprite):
    def __init__(self):
        """Initialises the character"""
        super().__init__()
        self.image = None
        self.rect = None

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
