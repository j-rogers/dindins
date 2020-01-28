import pygame

WIDTH = 1000
HEIGHT = 800
FPS = 30
ASSETS = '../assets'

# Colours
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (192, 192, 192)
WHITE = (255, 255, 255)

# Custom events
PAUSE = pygame.USEREVENT + 1
RESUME = PAUSE + 1
HIDE = RESUME + 1
RENDER = HIDE + 1
OBJECTIVE = RENDER + 1