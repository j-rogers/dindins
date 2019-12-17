import pygame

from dindins.settings import *


class Lucy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/lucy/lucy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = 'right'

    def _flip(self, direction):
        if self.direction != direction:
            self.image = pygame.transform.flip(self.image, True, False)
            self.direction = direction

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
            self._flip('left')
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
            self._flip('right')
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5

        self.rect.x += self.speedx
        self.rect.y += self.speedy
