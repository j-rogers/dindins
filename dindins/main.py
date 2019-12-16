import pygame

from dindins.lucy import Lucy


class DinDins:
    def __init__(self):
        """Initilises game"""
        # Init pygame and set running to true
        pygame.init()
        self._running = True

        # Build root display
        self._rootdisplay = pygame.display.set_mode((500, 200))

        # Set up clock
        self._fps = 60
        self._clock = pygame.time.Clock()

        # Set up initial sprites
        self._allsprites = pygame.sprite.Group()
        player = Lucy()
        self._allsprites.add(player)

    def _cleanup(self):
        """Cleans up and quits pygame"""
        pygame.quit()

    def _handle(self, event):
        """Event handler"""
        if event.type == pygame.QUIT:
            self._running = False

    def _render(self):
        self._rootdisplay.fill((0,0,0))
        self._allsprites.draw(self._rootdisplay)
        pygame.display.flip()

    def _update(self):
        self._allsprites.update()

    def run(self):
        """Runs the game"""
        while self._running:
            self._clock.tick(self._fps)
            for event in pygame.event.get():
                self._handle(event)
            self._render()
            self._update()

        self._cleanup()


if __name__ == '__main__':
    game = DinDins()
    game.run()
