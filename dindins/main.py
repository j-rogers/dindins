import pygame

from dindins.lucy import Lucy
from dindins.settings import *
from dindins.gui import *


class MainMenu(pygame.Surface):
    def __init__(self):
        super().__init__((WIDTH, HEIGHT))

        self.text = []
        self.buttons = []

        title = Text.render('Din Dins', RED, (WIDTH / 2, HEIGHT / 8), size=50)
        playbtn = Button('Play', (WIDTH / 2, HEIGHT / 2), action=self._rungame)
        optionsbtn = Button('Options', (WIDTH / 2, HEIGHT / 2 + 110))

        self.text.append(title)
        self.buttons.append(playbtn)
        self.buttons.append(optionsbtn)

    def _rungame(self):
        pass

    def render(self):
        for surf, rect in self.text:
            self.blit(surf, rect)

        for button in self.buttons:
            button.render()
            self.blit(button, button.rect)


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

    def _render(self, screen):
        """Renders specified items

        Renders and updates all specified items. Sprites use the pygame.sprite.Group object to execute all draw and
        update calls. Objects and text are rendered/updated seperately.

        Args:
            sprites: pygame.sprite.Group object containing all sprites to be rendered
            text: Simple text boxes to be rendered
            objects: Any object with an update() method
        """
        self._rootdisplay.fill(BLACK)
        screen.render()
        self._rootdisplay.blit(screen, (0, 0))

        pygame.display.update()
        #pygame.display.flip()

    def run(self):
        """Displays the main menu"""
        screen = MainMenu()
        while self.running:
            # Handlers
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self._handle(event)
            self._render(screen)

        self._cleanup()

    def run_game(self):
        text = []
        sprites = pygame.sprite.Group()
        # Set up initial sprites
        player = Lucy()
        sprites.add(player)

        test = DialogueBox('hello there i would like to test the capability of my text wrapping logic', RED, (WIDTH / 2, HEIGHT * 0.5))
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
