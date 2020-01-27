"""GUI Objects

This file contains objects used to give the user a GUI. This includes text, buttons, and dialogue boxes.

Author: Josh Rogers
"""

import pygame
from math import ceil

from dindins.settings import *


class Text:
    """Text

    This class provides a simple helper method to produce the pygame text and rect objects required for displaying text
    on a screen. The text object contains the pygame.Surface object the text is rendered on to, and the rect object is
    used for positioning the text.
    """
    @staticmethod
    def render(text, fg, pos, bg=None, font='freesansbold.ttf', size=18):
        """Creates the text objects

        Args:
            text: String of text to display
            fg: Text colour
            pos: (x, y) coordinates of center of text
            bg: Background colour (defaults to None)
            font: Font to use for text (defaults to freesansbold.ttf)
            size: Size of text (defaults to 18)

        Returns:
            A tuple of the text and rect objects
        """
        font = pygame.font.Font(font, size)
        text = font.render(text, True, fg, bg)
        rect = text.get_rect()
        rect.center = pos
        return text, rect


class Button(pygame.Surface):
    """Button

    A button is essentially a filled rectangle with text that executes an action when clicked.

    Attributes:
        rect: Rect/position of the button
        text_surface: Text surface of the button
        text_rect: Position of the text on the button
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
        """Renders the button

        Renders the button and checks if the mouse is hovering over the button and/or has been clicked. If the mouse is
        hovering over the button then the background should be changed to the active colour. If the button is clicked
        then it's stored action will be called.
        """
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Get x, y to position rect
        x, y = self.rect.center
        x -= self.width / 2
        y -= self.height / 2

        # Check if mouse is over button
        if x + self.width > mouse[0] > x and y + self.height > mouse[1] > y:
            # Change to active colour
            self.fill(self.ac)

            # Check if button was clicked
            if click[0] and self.action:
                self.action()
        else:
            # Set to inactive colour
            self.fill(self.ic)

        # Render text onto button
        self.blit(self.text_surface, self.text_rect)


class DialogueBox(pygame.Surface):
    """Dialogue box

    The dialogue box presents text to the user in a typewriter fashion. That is, each character is printed one at a
    time. If the character would go over the edge of the box,then it is instead printed to a newline.

    Attributes:
        rect: Position of the box
        fg: Colour of text
        bg: Background colour of box
        width: Width of the box
        height: Height of the box
        buffer: Characters remaining to be printed to screen
        typed: List of lines that have been printed to the screen
        finished: Boolean that indicates that the user has pressed space to close the box
    """
    def __init__(self, text, pos, fg=BLACK, bg=GREY, width=500, height=100):
        """Creates the dialogue box

        Args:
            text: String to be printed
            fg: Colour of text
            pos: Position of box
            bg: Background colour of box (defaults to GREEN)
            width: Width of box (defaults to 500)
            height: Height of box (defaults to 100)
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

        # Flag to know when finished
        self.finished = False

        # Pause while box is up
        pygame.event.post(pygame.event.Event(PAUSE, {}))

    def render(self):
        """Renders the dialogue box

        One at a time the characters in the buffer are printed on the box. If a character would go over the edge of the
        box it is instead printed on a newline. This continues until the buffer is empty. When this happens, the user is
        prompted to 'Press space to continue'. Pressing space will then close the box.
        """
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
            if w > self.width - 10:
                split = self.typed[-1].rsplit(' ', 1)
                self.typed[-1] = split[-2:][0]
                self.typed.append(split[-1])

        # Nothing left to print, tell user to press space to continue
        else:
            text, rect = Text.render('Press space to continue...', self.fg, (self.width * 0.8, self.height - 10), size=12)
            self.blit(text, rect)

            if keystate[pygame.K_SPACE]:
                self.finished = True
                pygame.event.post(pygame.event.Event(RESUME, {}))

        # Print out each line
        y = 0
        for line in self.typed:
            text, rect = Text.render(line, self.fg, (0, 0))
            self.blit(text, (10, y))
            y += 20


class StaminaBar(pygame.Surface):
    def __init__(self, pos, stamina, width=150, height=25):
        super().__init__((width, height))
        self.rect = self.get_rect()
        self.rect.center = pos

        self.width = width
        self.height = height

        self.stamina = stamina
        self.blocked = False

    def render(self):
        self.fill(WHITE)
        remaining = pygame.Surface((ceil((self.stamina / 100) * self.width), self.height))
        remaining.fill(RED)

        self.blit(remaining, remaining.get_rect())
