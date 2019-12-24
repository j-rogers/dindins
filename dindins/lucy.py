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
        self.index = 0

        # Idle animation
        self.idle = [
            pygame.image.load(f'{ASSETS}/lucy/idle/idle1.png'),
            pygame.image.load(f'{ASSETS}/lucy/idle/idle1.png'),
            pygame.image.load(f'{ASSETS}/lucy/idle/idle2.png'),
            pygame.image.load(f'{ASSETS}/lucy/idle/idle2.png'),
            pygame.image.load(f'{ASSETS}/lucy/idle/idle3.png'),
            pygame.image.load(f'{ASSETS}/lucy/idle/idle4.png')
        ]

        # Walking animation
        self.walk = [
            pygame.image.load(f'{ASSETS}/lucy/walk/walk1.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk2.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk3.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk4.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk5.png'),
            pygame.image.load(f'{ASSETS}/lucy/walk/walk6.png')
        ]

    def _flip(self, direction):
        """Flips the direction of Lucy

        Flips Lucy left or right if she is not already facing that way.

        Args:
            direction: String of 'left' or 'right'
        """
        if self.direction != direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction

    def _playanimation(self, animation):
        """Plays the specified animation

        Args:
            animation: List of images that create the animation
            index: Index that specifies what current image should be shown
        """
        # Reset the index if reached the end of the animation
        self.index = 0 if self.index == (len(animation) - 1) else self.index

        # Flip image if we are going left
        if self.direction == 'left':
            self.image = pygame.transform.flip(animation[self.index], True, False)
        else:
            self.image = animation[self.index]

        # Increase index
        self.index += 1

    def update(self):
        """Update sprite

        This method handles all the live updates for the sprite. This includes movement and object interaction.
        """
        # Stops Lucy from moving
        speed = 3
        self.speedx = 0
        self.speedy = 0

        # Get current keystate
        keystate = pygame.key.get_pressed()

        # Movement
        if keystate[pygame.K_LEFT]:
            self.speedx = -speed
            self._playanimation(self.walk)
            self._flip('left')
        if keystate[pygame.K_RIGHT]:
            self.speedx = speed
            self._playanimation(self.walk)
            self._flip('right')
        if keystate[pygame.K_UP]:
            self.speedy = -speed
            self._playanimation(self.walk)
        if keystate[pygame.K_DOWN]:
            self.speedy = speed
            self._playanimation(self.walk)

        # Apply movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Play idle animation when not moving
        if not keystate[pygame.K_LEFT] and not keystate[pygame.K_RIGHT] and not keystate[pygame.K_UP] and not keystate[pygame.K_DOWN]:
            self._playanimation(self.idle)



