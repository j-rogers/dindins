import pygame

from dindins.settings import *


class Text:
    def __init__(self, text, fg, bg=None, font='freesansbold.ttf', size=18):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, fg, bg)
        self.rect = self.text.get_rect()


class Button(Text):
    def __init__(self, text, fg, ic, ac, width, height, display, font='freesansbold.ttf', size=18, action=None):
        super().__init__(text, fg, font=font, size=size)

        self.ic = ic
        self.ac = ac
        self.width = width
        self.height = height
        self.display = display
        self.action = action

    def update(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Get x, y to position rect
        x, y = self.rect.center
        x -= self.width / 2
        y -= self.height / 2

        if x + self.width > mouse[0] > x and y + self.height > mouse[1] > y:
            pygame.draw.rect(self.display, self.ac, (x, y, self.width, self.height))

            if click[0] and self.action:
                self.action()
        else:
            pygame.draw.rect(self.display, self.ic, (x, y, self.width, self.height))


class DialogueBox(Text):
    def __init__(self, text, fg, display, bg=GREEN, font='freesansbold.ttf', size=18, width=500, height=100):
        # Init text
        super().__init__('', fg, bg, font, size)
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

        # Properties
        self.fg = fg
        self.bg = bg
        self.display = display
        self.width = width
        self.height = height

        # Set text buffer
        self.buffer = [character for character in text]
        self.typed = ['']

    def update(self):
        # Get x, y to position rect
        x, y = self.rect.center
        x -= 10
        y -= self.height / 2
        pygame.draw.rect(self.display, self.bg, (x, y, self.width, self.height))

        if self.buffer:
            char = self.buffer.pop(0)
            self.typed[-1] += char
            w, h = self.font.size(self.typed[-1])
            if w > self.width:
                split = self.typed[-1].rsplit(' ', 1)
                self.typed[-1] = split[-2:][0]
                self.typed.append(split[-1])

        for line in self.typed:
            self.display.blit(self.font.render(line, True, self.fg), (x, y))
            y += 20




        #if self.index != (len(self.buffer) + 1):
        #    text = ''.join(self.buffer[0:self.index])
        #    w, h = self.font.size()
        #    if w > self.width:
        #        splittext = text.rsplit(' ', 1)
        #    self.text = self.font.render(text, True, self.fg)
        #    self.index += 1
