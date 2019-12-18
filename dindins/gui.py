import pygame


class Text:
    def __init__(self, text, fg, bg=None, font='freesansbold.ttf', size=18):
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, fg, bg)
        self.rect = self.text.get_rect()

class Button(Text):
    def __init__(self, text, fg, ic, ac, width, height, display, font='freesansbold.ttf', size=18):
        super().__init__(text, fg, font=font, size=size)

        self.ic = ic
        self.ac = ac
        self.width = width
        self.height = height
        self.display = display

    def update(self):
        mouse = pygame.mouse.get_pos()
        x, y = self.rect.center
        x -= self.width / 2
        y -= self.height / 2
        if x + self.width > mouse[0] > x and y + self.height > mouse[1] > y:
            pygame.draw.rect(self.display, self.ac, (x, y, self.width, self.height))
        else:
            pygame.draw.rect(self.display, self.ic, (x, y, self.width, self.height))

    def center(self, x, y):
        self.rect.center = (())