import pygame

class Lucy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('../assets/lucy/lucy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (250, 100)

    def update(self):
        #self.rect.x += 5
        pass