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

    def _cleanup(self):
        """Cleans up and quits pygame"""
        pygame.quit()
        exit(0)

    def _handle(self, event):
        """Event handler"""
        if event.type == pygame.QUIT:
            self.running = False

    def _update(self, sprites=None, text=None, objects=None):
        """Renders specified items

        Renders and updates all specified items. Sprites use the pygame.sprite.Group object to execute all draw and
        update calls. Objects and text are rendered/updated seperately.

        Args:
            sprites: pygame.sprite.Group object containing all sprites to be rendered
            text: Simple text boxes to be rendered
            objects: Any object with an update() method
        """
        self._rootdisplay.fill(BLACK)

        if sprites:
            sprites.update()
            sprites.draw(self._rootdisplay)

        for object in objects:
            object.update()

        for t in text:
            self._rootdisplay.blit(t.text, t.rect)

        pygame.display.update()
        #pygame.display.flip()

    def run(self):
        """Displays the main menu"""
        text = []
        buttons = []

        # Title
        title = Text('Din Dins', RED, size=50)
        title.rect.center = (WIDTH / 2, HEIGHT / 8)
        text.append(title)

        # Play button
        play = Button('Play', RED, GREEN, BLUE, 100, 100, self._rootdisplay,  action=self.run_game)
        play.rect.center = (WIDTH / 2, HEIGHT / 2)
        text.append(play)
        buttons.append(play)

        # Options button
        options = Button('Options', RED, GREEN, BLUE, 100, 100, self._rootdisplay)
        options.rect.center = (WIDTH / 2, HEIGHT / 2 + 110)
        text.append(options)
        buttons.append(options)

        while self.running:
            # Handlers
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self._handle(event)
            self._update(text=text, objects=buttons)

        self._cleanup()

    def run_game(self):
        text = []
        sprites = pygame.sprite.Group()
        # Set up initial sprites
        player = Lucy()
        sprites.add(player)

        test = DialogueBox('hello this is a test hello this is a test', RED, self._rootdisplay)
        text.append(test)

        while self.running:
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self._handle(event)

            self._update(sprites=sprites, text=text, objects=text)

        self._cleanup()


if __name__ == '__main__':
    game = DinDins()
    game.run()
