from time import sleep
import pygame
from pygame.locals import QUIT, KEYDOWN
from constants import WINDOW_DIMENSIONS, FLOOR_IMAGE, WALL_IMAGE, LEVEL_FILE, PLAYER_PIC
from constants import PLAYER_COORDINATES, BOSS_PIC, NEEDLE_PIC, TUBE_PIC, ETHER_PIC
from constants import CARCASS, VICTORY, FAILURE
from labyrinth import Labyrinth
from characters import Boss, Player
from item import Items


class Game:
    """ Class used to play the game. """

    # We start Pygame
    pygame.init()
    pygame.font.init()
    # We prepare the font of our caption to indicate how many items we picked
    # up
    myfont = pygame.font.SysFont(None, 40)

    # We display the window
    square_window = pygame.display.set_mode(WINDOW_DIMENSIONS)

    # We make the labyrinth
    labyrinth = Labyrinth(FLOOR_IMAGE, WALL_IMAGE, LEVEL_FILE)
    labyrinth.initialize_labyrinth(square_window)

    # We initialize McGyver and the gatekeeper
    mac = Player(PLAYER_PIC, PLAYER_COORDINATES)
    gatekeeper = Boss(BOSS_PIC, labyrinth.BOSS_COORDINATES)

    # We initialize the three components of the serynge
    needle = Items(NEEDLE_PIC, labyrinth)
    tube = Items(TUBE_PIC, labyrinth)
    ether = Items(ETHER_PIC, labyrinth)

    # Displays Items
    def display_items(self, item):
        self.square_window.blit(item.image, item.coordinates)

    # Display characters
    def display_character(self, character):
        self.square_window.blit(character.head, character.coordinates)

    def main(self):
        """ Function that runs the game """
        is_running = True
        # Loop of the game
        while is_running:

            # Displays the game
            self.labyrinth.display_labyrinth(self.square_window)
            self.display_character(self.mac)
            self.display_character(self.gatekeeper)
            for item in Items.LIST_OF_ITEMS:
                self.display_items(item)
            pygame.display.flip()

            # What happens when we meet the gatekeeper
            if self.mac.coordinates in self.labyrinth.FIGHT_POSITION:
                if self.mac.count == 3:
                    self.mac.neutralize(
                        self.labyrinth,
                        self.gatekeeper,
                        self.labyrinth.EXIT_POSITION)
                else:
                    self.gatekeeper.lose(self.mac, CARCASS)
                    self.square_window.blit(
                        self.mac.head, self.mac.coordinates)
                    is_running = False

            # Reaching the exit position
            if self.mac.coordinates == self.labyrinth.EXIT_POSITION:
                self.mac.victorious = True
                is_running = False

            # Events detection
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_running = False
                if event.type == KEYDOWN:
                    x, y = self.mac.move(event)

                    # Square where we can walk, or with a serynge component, or
                    # wall so we can't use it
                    if (x, y) in [
                            item.coordinates for item in Items.LIST_OF_ITEMS]:
                        self.mac.count += 1
                        Items.LIST_OF_ITEMS = [
                            item for item in Items.LIST_OF_ITEMS if item.coordinates != (
                                x, y)]
                        moving = True
                        print(self.mac.count)
                    else:
                        moving = False

                    if self.labyrinth.reachable((x / 40, y / 40)):
                        moving = True

                    #  Moving means replace the position of Mac by en empty square
                    # Moving also means replacing an empty square by the
                    # position of Mac
                    if moving:
                        self.labyrinth.void.append(self.mac.coordinates)
                        self.mac.coordinates = (x, y)

            txt = self.myfont.render(
                str(self.mac.count) + "items picked up!", False, (255, 255, 255))
            self.square_window.blit(txt, (0, 0))
            pygame.display.flip()

        # Outcome of the game
        if self.mac.victorious:
            path = VICTORY
        else:
            path = FAILURE

        # Showing the outcome notification
        notification = pygame.image.load(path).convert()
        self.square_window.blit(notification, (100, 300))
        pygame.display.flip()

        #  Waiting 1 seconds before closing the window
        sleep(1)


# Detection of the entry point of the game : confirming that the class
# contains the main method
if __name__ == "__main__":
    game = Game()
    game.main()
