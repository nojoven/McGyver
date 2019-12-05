import pygame
from constants import FIGHT_POSITION, EXIT_POSITION, PLAYER_COORDINATES, BOSS_COORDINATES

"""

Constructor of the Labyrinth object

"""


class Labyrinth:

    def __init__(self, ground_image, wall_image_path, model_path):

        self.ground = ground_image
        self.wall = wall_image_path
        self.source = model_path
        self.void = []

    """ Function that initialize the labyrinth """

    def initialize_labyrinth(self, screen):
        """ Opens and read our model """
        with open(self.source, "r") as data:
            model = data.read()

        """ Loop on every line in lab.txt """
        for j, line in enumerate(model.split("\n")):
            """ We evaluate for each letter if it is a wall or a ground. """
            for i, letter in enumerate(line):
                if letter == "X":
                    image_path = self.wall
                elif letter == "E":
                    EXIT_POSITION = (i * 40, j * 40)
                    self.void.append((i * 40, j * 40))
                elif letter == "G":
                    BOSS_COORDINATES = (i * 40, j * 40)
                    FIGHT_POSITION = [(BOSS_COORDINATES[0] + 40, BOSS_COORDINATES[1]),
                                      (BOSS_COORDINATES[0] -
                                       40, BOSS_COORDINATES[1]),
                                      (BOSS_COORDINATES[0],
                                       BOSS_COORDINATES[1] - 40),
                                      (BOSS_COORDINATES[0],
                                       BOSS_COORDINATES[1] + 40)
                                      ]
                    self.void.append((i * 40, j * 40))

                else:
                    image_path = self.ground
                    self.void.append((i * 40, j * 40))
                square = pygame.image.load(image_path).convert()
                screen.blit(square, (i, j))
                i += 40
            j += 40

        """ Some special places to remove """
        self.void.remove(EXIT_POSITION)
        self.void.remove(PLAYER_COORDINATES)
        self.void.remove(BOSS_COORDINATES)

    """ Function that displays the labyrinth """

    def display_labyrinth(self, screen):
        with open(self.source, "r") as data:
            source = data.read()
        j = 0
        for line in source.split("\n"):
            i = 0
            for letter in line:
                if letter == "X":
                    image_path = self.wall
                else:
                    image_path = self.ground
                """ Load of the image """
                square = pygame.image.load(image_path).convert()
                """ Displays the image at the coordinates (i, j) with i pixels starting from the left and j pixels starting from the top """
                screen.blit(square, (i, j))

                i += 40
            j += 40
