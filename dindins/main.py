import pygame

from dindins.lucy import Lucy
from dindins.settings import *
from dindins.gui import *
from dindins.game_objects import *


class Screen(pygame.Surface):
    """Base Screen Object

    This provides the base screen object that other screens inherit off. It itself inherits from the pygame.Surface
    object so it can easily be rendered and interacted by other pygame objects. It includes lists of GUI elements that
    can be rendered, as well as an abstract update method, and a render method. The render method is not to be changed
    by child objects unless for good reason. The update method is to be implemented by the child object.

    Attributes:
        text: List of text to be rendered
        buttons: List of buttons to be rendered
        sprites: pygame.sprite.Group of sprites to be rendered
        dialogue: List of dialogue boxes to be rendered
    """
    def __init__(self):
        """Initiates pygame.Surface and attributes"""
        super().__init__((WIDTH, HEIGHT))
        self.rect = self.get_rect()
        self.rect.center = ((WIDTH / 2, HEIGHT / 2))

        self.text = []
        self.buttons = []
        self.sprites = pygame.sprite.Group()
        self.dialogue = []
        self.gameobjects = ObjectsGroup()

    def handle(self, event):
        """Handles events

        This method is to be implemented by the child object. The handler is used to process any events the current
        screen may be interested in. If no events are needed, then the implementation of this method can be omitted.

        Args:
            event: pygame.Event to be handled
        """
        pass

    def update(self):
        """Updates the screen

        This method is to be implemented by the child object. The update method is used to place any code that needs to
        be called once every frame. For example, game logic of holding down a directional key to move the screen
        up/down/left/right. It also indicates that the screen should be updated to a different screen. For example,
        clicking the 'Options' button on the main menu will cause the screen to be updated, no longer rendering the
        main menu but instead the options screen.

        Returns:
            This method must return the screen to be rendered. If no change of screen is needed then return self.
        """
        pass

    def render(self):
        """Renders all gui elements

        Renders each GUI element currently in the attribute lists.
        """
        # Clear screen
        self.fill(BLACK)

        # Text
        for surf, rect in self.text:
            self.blit(surf, rect)

        # Buttons
        for button in self.buttons:
            button.render()
            self.blit(button, button.rect)

        # Dialogue boxes
        for box in self.dialogue:
            if box.finished:
                self.dialogue.remove(box)
            else:
                box.render()
                self.blit(box, box.rect)

        # Game objects
        for object in self.gameobjects.objects:
            object.render()
            self.blit(object, object.rect)

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
        #self.dialogue.append(DialogueBox('hello there i would like to test the capabilities of my dialogue box thingy', (WIDTH / 2, HEIGHT / 2)))

        # Walls
        self.gameobjects.add(
            Wall((600, 400), 10, 500),  # Hallway east wall
            Wall((530, 645), 150, 10),  # Lobby south wall
            Wall((460, 595), 10, 100),  # Lobby west wall
            Wall((485, 545), 60, 10),   # Lobby north wall
            Wall((510, 350), 10, 400)   # Hallway west wall
        )

        # Doors
        self.gameobjects.add(
            Door((560, 645), 50, 20, 'Scary door')
        )

    def handle(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                objects = self.player.rect.collidelistall(self.gameobjects.interactables)
                if objects:
                    for i in objects:
                        self.gameobjects.interactables[i].interact()

    def update(self):
        """Updates the screen

        To keep the 'camera' centered on Lucy, we move the objects on the screen instead of the Lucy sprite. So we
        update rect x and y coordinates when the directional keys are pressed to achieve this.

        Returns:
            The screen to be rendered
        """
        speed_x = 0
        speed_y = 0

        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            speed_x = 3
        if keystate[pygame.K_RIGHT]:
            speed_x = -3
        if keystate[pygame.K_UP]:
            speed_y = 3
        if keystate[pygame.K_DOWN]:
            speed_y = -3

        # Shift wall rects
        for object in self.gameobjects.objects:
            object.rect.move_ip(speed_x, speed_y)

        # Reset walls if collision occurred
        if self.player.rect.collidelistall(self.gameobjects.colliders):
            for object in self.gameobjects.objects:
                object.rect.move_ip(-1 * speed_x, -1 * speed_y)

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

    def _handle(self, event, screen):
        """Event handler

        The DinDins event handler processes events that concern the application as a whole, such as closing the game.
        Otherwise it passes the event to the current screens handler.
        """
        if event.type == pygame.QUIT:
            self.running = False
        else:
            screen.handle(event)

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
                self._handle(event, screen)

            screen = screen.update()
            self._render(screen)

        self._cleanup()


if __name__ == '__main__':
    game = DinDins()
    game.run()
