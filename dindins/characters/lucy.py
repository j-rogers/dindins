import pygame

from dindins.settings import *
from dindins.objects import Animated


class Lucy(Animated):
    def __init__(self):
        """Initialises Lucy"""
        # Init sprite, set direction and location
        super().__init__((WIDTH / 2, HEIGHT / 2), pygame.image.load(f'{ASSETS}/lucy/idle/lucy_idle_down.png'), 'lucy', boundingbox='image')

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
        if not self.pause:
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
