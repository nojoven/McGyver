import pygame

class Labyrinth:
    # Arrival of the guardian, list of the squares protected by him and
    # departure square coordinates
    EXIT_POSITION = ()
    FIGHT_POSITION = []
    BOSS_COORDINATES = ()
    PLAYER_COORDINATES = ()

    def __init__(self, ground_image, wall_image_path, model_path):
        """ Constructor of the Labyrinth object """
        self.ground = ground_image
        self.wall = wall_image_path
        self.source = model_path
        self.obstacles = []
        self.void = []

    def initialize_labyrinth(self, screen):
        """ Function that initialize the labyrinth """
        # Opens and read our model
        with open(self.source, "r") as data:
            model = data.read()

        # Loops on every line in lab.txt
        for j, line in enumerate(model.split("\n")):
            # We evaluate for each letter if it is a wall or a ground.
            for i, letter in enumerate(line):
                if letter == "X":
                    image_path = self.wall
                    self.obstacles.append((i, j))
                elif letter == "E":
                    self.EXIT_POSITION = (i * 40, j * 40)

                elif letter == "M":
                    self.PLAYER_COORDINATES = (i*40,j*40)

                elif letter == "G":
                    self.BOSS_COORDINATES = (i * 40, j * 40)
                    self.FIGHT_POSITION = [
                        (self.BOSS_COORDINATES[0] + 40,
                         self.BOSS_COORDINATES[1]),
                        (self.BOSS_COORDINATES[0] - 40,
                         self.BOSS_COORDINATES[1]),
                        (self.BOSS_COORDINATES[0],
                         self.BOSS_COORDINATES[1] - 40),
                        (self.BOSS_COORDINATES[0],
                         self.BOSS_COORDINATES[1] + 40)]
                else:
                    image_path = self.ground
                    self.void.append((i * 40, j * 40))
                square = pygame.image.load(image_path).convert()
                screen.blit(square, (i, j))
                i += 40
            j += 40

    def reachable(self, coords):
        """Function that returns True if the square where we want to go is not a wall"""
        return coords not in self.obstacles and (
            0 <= coords[0] < 15) and (0 <= coords[1] < 15)

    def display_labyrinth(self, screen):
        """ Function that displays the labyrinth """
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
                # Loading of the image
                square = pygame.image.load(image_path).convert()
                # Displays the image at the coordinates (i, j)
                # with i pixels starting from the left and j pixels starting
                # from the top
                screen.blit(square, (i, j))

                i += 40
            j += 40
