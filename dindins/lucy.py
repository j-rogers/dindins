import pygame

from dindins.settings import *


class Lucy(pygame.sprite.Sprite):
    def __init__(self):
        """Initialises Lucy"""
        # Init sprite, set direction and location
        super().__init__()
        self.image = pygame.image.load(f'{ASSETS}/lucy/lucy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = 'right'

        # Walking animation
        self.walk = [
            pygame.image.load(f'{ASSETS}/lucy/walk/walk1.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk2.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk3.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk4.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk5.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk6.png')
        ]
        self.walker = 0


    def _flip(self, direction):
        """Flips the direction of Lucy

        Flips Lucy left or right if she is not already facing that way.

        Args:
            direction: String of 'left' or 'right'
        """
        if self.direction != direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction

    def _walk(self):
        """Plays the walking animation"""
        # Reset walker index if needed
        self.walker = 0 if self.walker == 5 else self.walker

        # Flip animation if walking left
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.walk[self.walker], True, False)
        else:
            self.image = self.walk[self.walker]

        # Increase index
        self.walker += 1

    def update(self):
        """Update sprite

        This method handles all the live updates for the sprite. This includes movement and object interaction.
        """
        # Default/Idle
        self.speedx = 0
        self.speedy = 0

        # Get current keystate
        keystate = pygame.key.get_pressed()

        # Movement
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
            self._walk()
            self._flip('left')
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            self._walk()
            self._flip('right')
        if keystate[pygame.K_UP]:
            self.speedy = -5
            self._walk()
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
            self._walk()

        self.rect.x += self.speedx
        self.rect.y += self.speedy

