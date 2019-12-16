import pygame


class DinDins:
    def __init__(self):
        """Initilises game"""
        pygame.init()
        self._running = True
        self._rootdisplay = pygame.display.set_mode((500, 200))

    def _cleanup(self):
        """Cleans up and quits pygame"""
        pygame.quit()

    def _handle(self, event):
        """Event handler"""
        if event.type == pygame.QUIT:
            self._running = False

    def run(self):
        """Runs the game"""
        while self._running:
            for event in pygame.event.get():
                self._handle(event)

        self._cleanup()


if __name__ == '__main__':
    game = DinDins()
    game.run()
