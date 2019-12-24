import pygame

from dindins.lucy import Lucy
from dindins.settings import *
from dindins.gui import *


class Screen(pygame.Surface):
    def __init__(self):
        super().__init__((WIDTH, HEIGHT))

        self.text = []
        self.buttons = []
        self.sprites = pygame.sprite.Group()

    def update(self):
        pass

    def render(self):
        # Clear screen
        self.fill(BLACK)

        # Text
        for surf, rect in self.text:
            self.blit(surf, rect)

        # Buttons
        for button in self.buttons:
            button.render()
            self.blit(button, button.rect)

        # Sprites
        self.sprites.update()
        self.sprites.draw(self)


class MainMenu(Screen):
    def __init__(self):
        super().__init__()

        # List of text and buttons
        self.text = []
        self.buttons = []

        # GUI elements
        title = Text.render('Din Dins', RED, (WIDTH / 2, HEIGHT / 8), size=50)
        playbtn = Button('Play', (WIDTH / 2, HEIGHT / 2), action=self._rungame)
        optionsbtn = Button('Options', (WIDTH / 2, HEIGHT / 2 + 110), action=self._options)

        # Add elements to be rendered
        self.text.append(title)
        self.buttons.append(playbtn)
        self.buttons.append(optionsbtn)

        # Flags for displaying other screens
        self.rungame = False
        self.options = False

    def _options(self):
        self.options = True

    def _rungame(self):
        self.rungame = True

    def update(self):
        if self.rungame:
            return GameScreen()
        elif self.options:
            return OptionsMenu()
        else:
            return self


class GameScreen(Screen):
    def __init__(self):
        super().__init__()

        self.player = Lucy()
        self.sprites.add(self.player)

    def update(self):
        return self


class OptionsMenu(Screen):
    def __init__(self):
        super().__init__()

    def update(self):
        return self


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
        screen.render()
        self._rootdisplay.blit(screen, (0, 0))

        pygame.display.flip()

    def run(self):
        """Displays the main menu"""
        screen = MainMenu()
        while self.running:
            # Handlers
            self._clock.tick(FPS)
            for event in pygame.event.get():
                self._handle(event)

            screen = screen.update()
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
