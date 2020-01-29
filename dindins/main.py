from dindins.characters.lucy import Lucy
from dindins.characters.juice import Juice
from dindins.objects import *


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
        self.dialogue = []
        self.player = pygame.sprite.GroupSingle()
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

        # Game objects
        self.gameobjects.update()
        self.gameobjects.draw(self)

        # Player
        self.player.update()
        self.player.draw(self)

        # Dialogue boxes
        for box in self.dialogue:
            if box.finished:
                self.dialogue.remove(box)
            else:
                box.render()
                self.blit(box, box.rect)


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
    """In game screen

    This screen handles all interactions and rendering for the DinDins game. The update method is used to move objects
    around the screen to keep the camera centered on the player. The handle method handles in game events such as
    object interaction, pausing/resuming, and hiding.

    Attributes:
        player: pygame.sprite.GroupSingle containing the sprite of the player
        speed: Int describing the movement speed in pixels per frame
        hiding: Boolean indicating if the player is currently hiding
        temp: Variable used to temporarily store any information
        gameobjects: pygame.sprite.Group of every other object in the game
    """
    def __init__(self):
        """Loads initial objects"""
        super().__init__()

        # Add player character
        self.player.add(Lucy())

        # State variables
        self.speed = 3
        self.stamina = StaminaBar((100, 750), 100)
        self.hiding = False
        self.paused = False
        self.temp = None

        self.buttons.append(self.stamina)

        self.objectives = [
            'eat_food',
            'hide_under_bed',
            'go_to_kitchen',
            'nothing'
        ]

        # Floor
        self.gameobjects.add(
            tileset((590, -226), 10, 7, 'living_floor'),
            tileset((495, 18), 7, 7, 'courtyard_floor', type='tile'),
            tileset((580, 630), 3, 2, 'lobby_floor'),
            tileset((589, 534), 2, 25, 'hallway_floor'),
            tileset((493, 94), 1, 2, 'alcove_floor'),
            tileset((495, 376), 7, 5, 'bedroom_floor', type='carpet')
        )

        # Walls
        self.gameobjects.add(
            tile((600, 210), 11, 875, 'hallway_east', boundingbox=(-1, 438, 5, 438)),  # Hallway east wall
            tile((535, 645), 140, 10, 'lobby_south', boundingbox=(70, 1, 70, 1)),  # Lobby south wall
            tile((470, 595), 10, 100, 'lobby_west', boundingbox=(5, 50, -2, 50)),  # Lobby west wall
            tile((490, 545), 50, 10, 'lobby_north', boundingbox=(25, 19, 5, -18)),   # Lobby north wall
            tile((510, 470), 10, 160, 'hallway_west_lobbytobedroom', boundingbox=(5, 79, -2, 59)),  # Hallway west wall (lobby -> bedroom)
            tile((380, 395), 250, 10, 'bedroom_south', boundingbox=(125, 1, 125, 1)),  # Bedroom south wall
            tile((510, 215), 10, 220, 'hallway_west_bedroomtostudy', boundingbox=(3, 110, -2, 90)),  # Hallway west wall (bedroom -> study)
            tile((380, 195), 250, 10, 'bedroom_north', boundingbox=(125, 19, 125, -18)),  # Bedroom north wall
            tile((260, 295), 10, 200, 'bedroom_west', boundingbox=(5, 100, -2, 100)),  # Bedroom west wall
            tile((480, 110), 50, 10, 'alcove_south', boundingbox=(25, 1, 25, 1)),    # Alcove south wall
            tile((450, 65), 10, 100, 'alcove_west', boundingbox=(5, 50, -2, 50)),  # Alcove west wall
            tile((480, 20), 50, 10, 'alcove_north', boundingbox=(25, 19, 25, -18)),    # Alcove north wall
            tile((510, -100), 10, 250, 'hallway_west_glass', boundingbox=(5, 120, -2, 100)),  # Hallway west wall, looking into courtyard
            tile((385, -220), 250, 10, 'living_south_glass', boundingbox=(125, 1, 125, 1)),   # Living room south wall, looking into courtyard
            tile((259, -219), 11, 502, 'courtyard_kitchen_west', boundingbox=(5, 250, -2, 250)),   # Courtyard and kitchen west wall
            tile((355, 30), 200, 10, 'study_north_glass'),  # Study north wall, looking into courtyard
            tile((435, -465), 355, 10, 'living_north', boundingbox=(178, 19, 178, -18)),     # Living room/kitchen north wall
            tile((610, -345), 10, 250, 'living_east', boundingbox=(-1, 125, 5, 125))      # Living room east wall
        )

        # Doors
        greysurface = pygame.Surface((50, 20))
        greysurface.fill(GREY)
        self.gameobjects.add(
            DialogueBoxObject((560, 645), greysurface, 'Scary people come through this door. I would never dare go out there.', 'front_door'),     # Front door
            DialogueBoxObject((510, 450), pygame.transform.rotate(greysurface, 90), 'My humans litterbox is in there.', 'bathroom_door_hallway'),    # Bathroom door (from hallway)
            DialogueBoxObject((470, 595), pygame.transform.rotate(greysurface, 90), 'I used to sleep in this room, but now it\'s never open.', 'storage_door'),   # Room 1
            DialogueBoxObject((440, 395), greysurface, 'My humans litterbox is in there.', 'bathroom_door_bedroom'),  # Bathroom door (from bedroom)
            DialogueBoxObject((320, 395), greysurface, 'This goes to a courtyard. There was once a trapped bird in there.', 'courtyard_door_bedroom'),   # Bedroom courtyard
            DialogueBoxObject((510, 150), pygame.transform.rotate(greysurface, 90), 'This is where my humans spend most of their time. It\'s only open when they\'re home.', 'study_door'),          # Study
            DialogueBoxObject((325, -485), pygame.image.load(f'{ASSETS}/objects/door.png'), 'Scary sounds come from this door. But my humans also come through here.', 'garage_door')    # Garage
        )

        # Other objects
        self.gameobjects.add(
            BaseObject((425, -270), pygame.image.load(f'{ASSETS}/objects/rug2.png'), 'table_rug'),
            HideObject((425, -285), pygame.image.load(f'{ASSETS}/objects/table.png'), 'table', boundingbox=(28, 22, 28, 10)),
            BaseObject((340, 200), pygame.image.load(f'{ASSETS}/objects/dresser.png'), 'dresser1', boundingbox=(7, 18, 8, 1)),
            BaseObject((440, 200), pygame.image.load(f'{ASSETS}/objects/dresser.png'), 'dresser2', boundingbox=(6, 18, 7, 1)),
            BaseObject((585, -385), pygame.image.load(f'{ASSETS}/objects/tv.png'), 'tv', boundingbox=(18, 64)),
            BaseObject((375, -410), pygame.image.load(f'{ASSETS}/objects/bench1.png'), 'bench1', boundingbox=(7, 56, 5, 35)),
            BaseObject((278, -410), pygame.image.load(f'{ASSETS}/objects/bench2.png'), 'bench2', boundingbox=(7, 56, 5, 35)),
            BaseObject((325, -390), pygame.image.load(f'{ASSETS}/objects/rug1.png'), 'kitchen_rug'),
            BaseObject((518, -375), pygame.image.load(f'{ASSETS}/objects/rug3.png'), 'living_rug'),
            BaseObject((519, -380), pygame.image.load(f'{ASSETS}/objects/coffee_table.png'), 'coffee_table',  boundingbox=(10, 26, 5, 6)),
            BaseObject((585, -460), pygame.image.load(f'{ASSETS}/objects/lamp.png'), 'lamp', boundingbox='image'),
            BaseObject((585, -315), pygame.image.load(f'{ASSETS}/objects/plant.png'), 'plant', boundingbox=(20, 10)),
            BaseObject((455, -385), pygame.image.load(f'{ASSETS}/objects/couch.png'), 'couch', boundingbox=(7, 40, 10, 20)),
            BaseObject((283, 280), pygame.image.load(f'{ASSETS}/objects/wardrobe.png'), 'wardrobe', boundingbox=(18, 48, 5, 30)),
        )

        # Objective objects
        self.gameobjects.add(
            Bowls(self.objectives),
            Bed(self.objectives),
        )

        # Shift objects for initial positioning
        for object in self.gameobjects.sprites():
            object.move(-50, 800)

    def _collide(self):
        for object in self.gameobjects.colliders():
            if self.player.sprite.rect.colliderect(object.boundingbox):
                return True

    def handle(self, event):
        """Handles in game events

        This method handles all events in game. This includes pressing the space bar to interact with objects,
        pausing/resuming, and hiding.

        Args:
            event: pygame.Event object to handle
        """
        # Space to interact with objects
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Regular interaction
                if not self.paused and not self.hiding:
                    for object in self.gameobjects.interactables():
                        # Allows for interaction with collidable objects
                        if pygame.sprite.collide_rect_ratio(1.25)(self.player.sprite, object):
                            object.interact()

                # Stop hiding
                elif self.hiding and not self.paused:
                    # Resume player
                    self.player.sprite.pause = False
                    self.hiding = False
                    self.speed = 3

                    # Revert objects using saved offset
                    for object in self.gameobjects.sprites():
                        object.move(-1 * self.temp[0],  -1 * self.temp[1])

        # Pause the game
        elif event.type == PAUSE:
            self.paused = True
            self.speed = 0
            self.player.sprite.pause = True

        # Resume the game
        elif event.type == RESUME:
            self.paused = False
            self.speed = 3
            # Only show the player if they are not hiding
            if not self.hiding:
                self.player.sprite.pause = False

        # Hide
        # Hiding pauses only the player (not NPCs), and makes the player sprite transparent.
        elif event.type == HIDE:
            # Pause player
            self.player.sprite.pause = True
            self.speed = 0
            self.hiding = True

            # Make player transparent
            self.player.sprite.image = pygame.image.load(f'{ASSETS}/terrain/transparent.png')

            # If move is set to false then move camera to center of hiding object
            if not event.move:
                # Get player and object coordinates
                object = event.object.rect.center
                pos = self.player.sprite.rect.center

                # Calculate and save offset so we can revert when not hiding
                x = pos[0] - object[0]
                y = pos[1] - object[1]
                self.temp = (x, y)

                # Move objects
                for object in self.gameobjects.sprites():
                    object.move(x, y)

        # Render given objects
        elif event.type == RENDER:
            for object in event.objects:
                if type(object) == DialogueBox:
                    self.dialogue.append(object)

        # Objective completed
        elif event.type == OBJECTIVE:
            self.objectives.remove(event.objective)

            if self.objectives[0] == 'go_to_kitchen':
                self.gameobjects.add(Juice((555, -220)))

    def update(self):
        """Updates the screen

        To keep the 'camera' centered on Lucy, we move the objects on the screen instead of the Lucy sprite. So we
        update rect x and y coordinates when the directional keys are pressed to achieve this.

        Returns:
            The screen to be rendered
        """
        speed_x = 0
        speed_y = 0

        # Movement
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            speed_x = self.speed
        if keystate[pygame.K_RIGHT]:
            speed_x = self.speed * -1
        if keystate[pygame.K_UP]:
            speed_y = self.speed
        if keystate[pygame.K_DOWN]:
            speed_y = self.speed * -1

        # Sprinting
        # If Lucy runs out of stamina, she will be blocked until her stamina is full again.
        if keystate[pygame.K_LSHIFT] and not self.stamina.blocked:
            self.player.sprite.rate = 6
            speed_x *= 2
            speed_y *= 2
            self.stamina.stamina -= 1
            # Block sprinting if no stamina remaining
            if self.stamina.stamina == 0:
                self.stamina.blocked = True
        else:
            # Regain stamina when not sprinting
            if self.stamina.stamina < 100:
                self.stamina.stamina += 1
            # Unblock sprinting if full stamina
            else:
                self.stamina.blocked = False
            self.player.sprite.rate = 2

        # Shift all objects on x axis
        for object in self.gameobjects.sprites():
            object.move(speed_x, 0)

        # Reset objects if collision occurred
        if self._collide():
            for object in self.gameobjects.sprites():
                object.move(-1 * speed_x, 0)

        # Shift all objects on y axis
        for object in self.gameobjects.sprites():
            object.move(0, speed_y)

        # Reset objects if collision occurred
        if self._collide():
            for object in self.gameobjects.sprites():
                object.move(0, -1 * speed_y)

        return self


class OptionsMenu(Screen):
    def __init__(self):
        super().__init__()

    def update(self):
        return self


class DinDins:
    """Main loop

    This class contains the entry point and main loop of the game.

    Attributes:
        running: Boolean indicating if the game is running
        rootdisplay: pygame.display, the main window
        clock: pygame.time.Clock for setting FPS
    """
    def __init__(self):
        """Initialises game"""
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

        Args:
            event: pygame.event.Event to handle
            screen: Screen to pass event to
        """
        if event.type == pygame.QUIT:
            self.running = False
        else:
            screen.handle(event)

    def _render(self, screen):
        """Renders the screen

        Args:
            screen: Screen to be rendered
        """
        screen.render()
        self._rootdisplay.blit(screen, (0, 0))

        pygame.display.flip()

    def run(self):
        """Main game loop"""
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
