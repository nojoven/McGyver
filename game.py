from time import sleep
import pygame
from pygame.locals import QUIT, KEYDOWN
from constants import WINDOW_DIMENSIONS, FLOOR_IMAGE, WALL_IMAGE, LEVEL_FILE, PLAYER_PIC
from constants import PLAYER_COORDINATES, BOSS_PIC, BOSS_COORDINATES, NEEDLE_PIC, TUBE_PIC, ETHER_PIC
from constants import FIGHT_POSITION, EXIT_POSITION, CARCASS, VICTORY, FAILURE
from labyrinth import Labyrinth
from characters import Boss, Player
from item import Items

class Game:

    """ Start pygame """
    pygame.init()

    """ Display the window """
    square_window = pygame.display.set_mode(WINDOW_DIMENSIONS)

    """ Make the labyrinth"""
    level_components = Labyrinth(FLOOR_IMAGE, WALL_IMAGE, LEVEL_FILE)
    level_components.initialize_labyrinth(square_window)

    """ Initialize MacGyver and the gatekeeper """
    mac = Player(PLAYER_PIC, PLAYER_COORDINATES)
    gatekeeper = Boss(BOSS_PIC, BOSS_COORDINATES)

    """ Initialize the three components of the serynge """
    needle = Items(NEEDLE_PIC, level_components)
    tube = Items(TUBE_PIC, level_components)
    ether = Items(ETHER_PIC, level_components)

    """Displays Items"""
    def display_items(self, item):
        self.square_window.blit(item.image, item.coordinates)

    """Display Characters"""
    def display_character(self, character):
        self.square_window.blit(character.head, character.coordinates)

    def main(self):
        is_running = True
        """ Loop of the game """
        while is_running:

            """ Displays the game """
            self.level_components.display_labyrinth(self.square_window)
            self.display_character(self.mac)
            self.display_character(self.gatekeeper)
            for item in Items.LIST_OF_ITEMS:
                self.display_items(item)
            pygame.display.flip()

            """ What happens when we meet the gatekeeper """
            if self.mac.coordinates in FIGHT_POSITION:
                if self.mac.count == 3:
                    self.mac.neutralize(self.level_components, self.gatekeeper, EXIT_POSITION)
                else:
                    self.gatekeeper.lose(self.mac, CARCASS)
                    self.square_window.blit(self.mac.head, self.mac.coordinates)
                    is_running = False

            """ Reaching the exit position """
            if self.mac.coordinates == EXIT_POSITION:
                self.mac.victorious = True
                is_running = False

            """ Events detection """
            for event in pygame.event.get():
                if event.type == QUIT:
                    is_running = False
                if event.type == KEYDOWN:
                    x, y = self.mac.move(event)

                    """ Square where we can walk, or with a serynge component, or wall so we can't use it"""
                    if (x, y) in self.level_components.void:
                        self.level_components.void.remove((x, y))
                        moving = True

                    elif (x, y) in [item.coordinates for item in Items.LIST_OF_ITEMS]:
                        self.mac.count += 1
                        Items.LIST_OF_ITEMS = [
                            item for item in Items.LIST_OF_ITEMS if item.coordinates != (
                                x, y)]
                        moving = True

                    else:
                        moving = False

                    """ Moving """
                    if moving:
                        self.level_components.void.append(self.mac.coordinates)
                        self.mac.coordinates = (x, y)

        """ Outcome """
        if self.mac.victorious:
            path = VICTORY
        else:
            path = FAILURE

        """ Showing the outcome notification """
        notification = pygame.image.load(path).convert()
        self.square_window.blit(notification, (100, 300))
        pygame.display.flip()

        """ Waiting 1 seconds before closing the window """
        sleep(1)


if __name__ == "__main__":
    game = Game()
    game.main()
