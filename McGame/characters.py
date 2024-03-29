import pygame
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT


class Characters:
    """ Class that allows us to instanciate the chatacters """

    def __init__(self, pictures_path, coordinates):
        # constructor of the character
        self.head = pygame.image.load(pictures_path).convert_alpha()
        self.coordinates = coordinates


class Boss(Characters):
    """ Class of the boss """

    def __init__(self, image_path, coordinates):
        """constructor of the boss"""
        # We instanciate a character because a Boss is a Character
        Characters.__init__(self, image_path, coordinates)

    def lose(self, macgyver, dead_path):
        # Function to loose(MacGyver dies) if we don't have the serynge
        macgyver.head = pygame.image.load(dead_path).convert_alpha()


class Player(Characters):
    """ Class of the character.

    The player and the guardian are the characters.
    """

    def __init__(self, image_path, coordinates):
        """Constructor of the character"""
        Characters.__init__(self, image_path, coordinates)
        # number of items picked up by MacGyver
        self.count = 0
        # Flag that becomes True if we win
        self.victorious = False

    def move(self, event):
        # Allows the player to move from a square to another one
        x, y = self.coordinates
        if event.key == K_UP:
            y -= 40
        elif event.key == K_DOWN:
            y += 40
        elif event.key == K_RIGHT:
            x += 40
        elif event.key == K_LEFT:
            x -= 40
        else:
            pass
        return x, y

    def neutralize(self, labyrinth, the_boss):
        """ Getting rid of the boss

        Function that allows us to move on the dangerous squares where the boss would
        have killed us otherwise.
        """
        labyrinth.void.append(the_boss.coordinates)
