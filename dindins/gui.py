import pygame

from dindins.settings import *


class Text:
    """Text

    Attributes:
        font: pygame.Font containing font and size of the text
        text: pygame.Surface object containing the rendered text
        rect: Rect of the text surface
    """
    def __init__(self, text, fg, pos, bg=None, font='freesansbold.ttf', size=18):
        """Creates the text

        Args:
            text: String of text to display
            fg: Text colour
            pos: (x, y) coordinates of center of text
            bg: Background colour (defaults to None)
            font: Font to use for text (defaults to freesansbold.ttf)
            size: Size of text (defaults to 18)
        """
        self.font = pygame.font.Font(font, size)
        self.text = self.font.render(text, True, fg, bg)
        self.rect = self.text.get_rect()
        self.rect.center = pos

class Button(Text):
    """Button

    Attributes:
        ic: Inactive colour (defaults to GREEN)
        ac: Active colour (defaults to BLUE)
        width: Width of the button (defaults to 100)
        height: Height of the button (defaults to 100)
        display: Root display to draw to
        action: Callback for when button is pressed
    """
    def __init__(self, text, display, pos, fg=RED, ic=GREEN, ac=BLUE, width=100, height=100, font='freesansbold.ttf', size=18, action=None):
        """Creates the button

        Args:
            text: String to be displayed in the button
            display: Root display
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
        super().__init__(text, fg, pos, font=font, size=size)

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
    """Dialogue box

    Attributes:
        fg: Colour of text
        bg: Background colour of box
        display: Root display for drawing
        width: Width of the box
        height: Height of the box
        buffer: Characters remaining to be printed to screen
        typed: List of lines that have been printed to the screen
    """
    def __init__(self, text, fg, display, pos, bg=GREEN, width=500, height=100, font='freesansbold.ttf', size=18):
        """Creates the dialogue box

        Args:
            text: String to be printed
            fg: Colour of text
            display: Root display for drawing
            pos: Position of box
            bg: Background colour of box (defaults to GREEN)
            width: Width of box (defaults to 500)
            height: Height of box (defaults to 100)
            font: Font of text (defaults to freesansbold.ttf)
            size: Size of font/text
        """
        # Init text
        super().__init__('', fg, pos, bg=bg, font=font, size=size)
        self.rect.center = pos

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
        else:
            # show 'press space to continue'
            # check for space event
            pass

        for line in self.typed:
            self.display.blit(self.font.render(line, True, self.fg), (x, y))
            y += 20
