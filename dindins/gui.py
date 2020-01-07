import pygame

from dindins.settings import *


class Text:
    """Text"""
    @staticmethod
    def render(text, fg, pos, bg=None, font='freesansbold.ttf', size=18):
        """Creates the text

        Args:
            text: String of text to display
            fg: Text colour
            pos: (x, y) coordinates of center of text
            bg: Background colour (defaults to None)
            font: Font to use for text (defaults to freesansbold.ttf)
            size: Size of text (defaults to 18)
        """
        font = pygame.font.Font(font, size)
        text = font.render(text, True, fg, bg)
        rect = text.get_rect()
        rect.center = pos
        return text, rect


class Button(pygame.Surface):
    """Button

    Attributes:
        ic: Inactive colour (defaults to GREEN)
        ac: Active colour (defaults to BLUE)
        width: Width of the button (defaults to 100)
        height: Height of the button (defaults to 100)
        action: Callback for when button is pressed
    """
    def __init__(self, text, pos, fg=RED, ic=GREEN, ac=BLUE, width=100, height=100, font='freesansbold.ttf', size=18, action=None):
        """Creates the button

        Args:
            text: String to be displayed in the button
            pos: (x, y) coordinates of the center of the button
            fg: Text colour
            ic: Inactive colour
            ac: Active colour
            width: Width of the button
            height: Height of the button
            font: Font of the text
            size: Font size
            action: Callback for when the button is pressed
        """
        super().__init__((width, height))
        self.rect = self.get_rect()
        self.rect.center = pos
        self.text_surface, self.text_rect = Text.render(text, fg, (width / 2, height / 2), font=font, size=size)

        self.ic = ic
        self.ac = ac
        self.width = width
        self.height = height
        self.action = action

    def render(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Get x, y to position rect
        x, y = self.rect.center
        x -= self.width / 2
        y -= self.height / 2

        if x + self.width > mouse[0] > x and y + self.height > mouse[1] > y:
            self.fill(self.ac)

            if click[0] and self.action:
                self.action()
        else:
            self.fill(self.ic)

        self.blit(self.text_surface, self.text_rect)


class DialogueBox(pygame.Surface):
    """Dialogue box

    Attributes:
        fg: Colour of text
        bg: Background colour of box
        width: Width of the box
        height: Height of the box
        buffer: Characters remaining to be printed to screen
        typed: List of lines that have been printed to the screen
    """
    def __init__(self, text, pos, fg=RED, bg=GREEN, width=500, height=100, font='freesansbold.ttf', size=18):
        """Creates the dialogue box

        Args:
            text: String to be printed
            fg: Colour of text
            pos: Position of box
            bg: Background colour of box (defaults to GREEN)
            width: Width of box (defaults to 500)
            height: Height of box (defaults to 100)
            font: Font of text (defaults to freesansbold.ttf)
            size: Size of font/text
        """
        super().__init__((width, height))
        self.rect = self.get_rect()
        self.rect.center = pos

        # Properties
        self.fg = fg
        self.bg = bg
        self.width = width
        self.height = height

        # Set text buffer
        self.buffer = [character for character in text]
        self.typed = ['']

        self.finished = False

    def render(self):
        # Fill background
        self.fill(self.bg)

        keystate = pygame.key.get_pressed()

        # Characters left to print
        if self.buffer:
            # Get character and add it to typed
            char = self.buffer.pop(0)
            self.typed[-1] += char

            # Get size of text with added character
            text_surface, text_rect = Text.render(self.typed[-1], self.fg, (0, 0))
            w, h = text_surface.get_size()

            # Split and create new line if the character goes past box width
            if w > self.width:
                split = self.typed[-1].rsplit(' ', 1)
                self.typed[-1] = split[-2:][0]
                self.typed.append(split[-1])

        # Nothing left to print, tell user to press space to continue
        else:
            text, rect = Text.render('Press space to continue...', self.fg, (self.width * 0.8, self.height - 10), size=12)
            self.blit(text, rect)

            if keystate[pygame.K_SPACE]:
                self.finished = True

        # Print out each line
        y = 0
        for line in self.typed:
            text, rect = Text.render(line, self.fg, (0, 0))
            self.blit(text, (10, y))
            y += 20
