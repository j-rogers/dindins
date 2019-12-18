import pygame

from dindins.lucy import Lucy
from dindins.settings import *
from dindins.gui import *


class DinDins:
    def __init__(self):
        """Initilises game"""
        # Init pygame and set running to true
        pygame.init()
        self.running = True

        # Build root display
        self._rootdisplay = pygame.display.set_mode((WIDTH, HEIGHT))

        # Set up clock
        self._clock = pygame.time.Clock()

        # Group for sprites
        self._allsprites = pygame.sprite.Group()

        # Group for buttons
        self._buttons = []

    def _gameinit(self):
        # Set up initial sprites
        player = Lucy()
        self._allsprites.add(player)

    def _cleanup(self):
        """Cleans up and quits pygame"""
        pygame.quit()
        exit(0)

    def _handle(self, event):
        """Event handler"""
        if event.type == pygame.QUIT:
            self.running = False

    def _render(self):
        """Renders the game

        Render is used to display the sprites currently on screen in the game.
        """
        self._rootdisplay.fill((0,0,0))
        self._allsprites.draw(self._rootdisplay)
        pygame.display.flip()

    def _update(self):
        """Updates all functional objects

        Performs an update on all functional objects, such as (some) sprites (e.g. Lucy) and buttons.
        """
        self._allsprites.update()

        for button in self._buttons:
            button.update()

    def run(self):
        """Displays the main menu"""
        # Title
        title = Text('Din Dins', RED, size=50)
        title.rect.center = (WIDTH / 2, HEIGHT / 8)

        # Play button
        play = Button('Play', RED, GREEN, BLUE, 100, 100, self._rootdisplay,  action=self.run_game)
        play.rect.center = (WIDTH / 2, HEIGHT / 2)
        self._buttons.append(play)

        # Options button
        options = Button('Options', RED, GREEN, BLUE, 100, 100, self._rootdisplay)
        options.rect.center = (WIDTH / 2, HEIGHT / 2 + 110)
        self._buttons.append(options)

        while self.running:
            # Handlers
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self._handle(event)
            self._update()

            # Place objects on screen
            self._rootdisplay.blit(title.text, title.rect)
            self._rootdisplay.blit(play.text, play.rect)
            self._rootdisplay.blit(options.text, options.rect)

            # Update display
            pygame.display.update()

        self._cleanup()

    def run_game(self):
        self._gameinit()
        while self.running:
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self._handle(event)
            self._render()
            self._update()

        self._cleanup()

if __name__ == '__main__':
    game = DinDins()
    game.run()
