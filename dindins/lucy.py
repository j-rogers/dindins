import pygame

from dindins.settings import *


class Lucy(pygame.sprite.Sprite):
    def __init__(self):
        """Initialises Lucy"""
        # Init sprite, set direction and location
        super().__init__()
        self.image = pygame.image.load(f'{ASSETS}/lucy/idle/lucy_idle_down.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2 + 50, HEIGHT / 2)

        # Animation stuff
        self.direction = 'down'
        self.index = 0
        self.ticker = 0
        self.rate = 2

        # Idle
        self.idle = {
            'up': pygame.image.load(f'{ASSETS}/lucy/idle/lucy_idle_up.png'),
            'down': pygame.image.load(f'{ASSETS}/lucy/idle/lucy_idle_down.png'),
            'left': pygame.image.load(f'{ASSETS}/lucy/idle/lucy_idle_left.png'),
            'right': pygame.image.load(f'{ASSETS}/lucy/idle/lucy_idle_right.png')
        }

        # Walking animation
        self.walk = {
            'up': [
                pygame.image.load(f'{ASSETS}/lucy/walk/up/lucy_walk_up_1.png'),
                pygame.image.load(f'{ASSETS}/lucy/walk/up/lucy_walk_up_2.png')],
            'down': [
                pygame.image.load(f'{ASSETS}/lucy/walk/down/lucy_walk_down_1.png'),
                pygame.image.load(f'{ASSETS}/lucy/walk/down/lucy_walk_down_2.png')],
            'left': [
                pygame.image.load(f'{ASSETS}/lucy/walk/left/lucy_walk_left_1.png'),
                pygame.image.load(f'{ASSETS}/lucy/walk/left/lucy_walk_left_2.png')],
            'right': [
                pygame.image.load(f'{ASSETS}/lucy/walk/right/lucy_walk_right_1.png'),
                pygame.image.load(f'{ASSETS}/lucy/walk/right/lucy_walk_right_2.png')]
        }

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
        # Get current keystate
        keystate = pygame.key.get_pressed()

        # Set animation and direction of Lucy
        # If up/down and either left or right are pressed, the up/down animation should be used. So, the left/right
        # animations are only used if up or down are NOT being pressed. Additionally, the ticker should be reset if we
        # are changing directions, in order to immediately play the new animation.
        if keystate[pygame.K_LEFT] and not (keystate[pygame.K_UP] or keystate[pygame.K_DOWN]):
            self.ticker = 0 if self.direction != 'left' else self.ticker
            self.direction = 'left'
            self._playanimation(self.walk[self.direction])
        if keystate[pygame.K_RIGHT] and not (keystate[pygame.K_UP] or keystate[pygame.K_DOWN]):
            self.ticker = 0 if self.direction != 'right' else self.ticker
            self.direction = 'right'
            self._playanimation(self.walk[self.direction])
        if keystate[pygame.K_UP]:
            self.ticker = 0 if self.direction != 'up' else self.ticker
            self.direction = 'up'
            self._playanimation(self.walk[self.direction])
        if keystate[pygame.K_DOWN]:
            self.ticker = 0 if self.direction != 'down' else self.ticker
            self.direction = 'down'
            self._playanimation(self.walk[self.direction])

        # Play idle animation when not moving
        if not keystate[pygame.K_LEFT] and not keystate[pygame.K_RIGHT] and not keystate[pygame.K_UP] and not keystate[pygame.K_DOWN]:
            self.image = self.idle[self.direction]
            self.ticker = 0



