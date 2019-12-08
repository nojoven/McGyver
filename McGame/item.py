import random
import pygame


class Items:
    """This class allows us to instantiate items (the components of the serynge)."""
    # We make a list to store the items picked-up
    LIST_OF_ITEMS = []

    def __init__(self, image_path, labyrinth):
        """ Constructor of the Items object"""
        self.image = pygame.image.load(image_path).convert_alpha()
        self.coordinates = (0, 0)
        self.position_items(labyrinth)
        Items.LIST_OF_ITEMS.append(self)

    def position_items(self, labyrinth):
        """ Function used to position the items on their squares randomly """
        self.coordinates = random.choice(labyrinth.void)
        labyrinth.void.remove(self.coordinates)
