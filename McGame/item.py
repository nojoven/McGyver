import random
import pygame

"""

This class allows us to instanciate items (the components of the serynge).

"""


class Items:
    LIST_OF_ITEMS = []
    """ constructor of the Items object """
    def __init__(self, image_path, labyrinth):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.coordinates = (0, 0)
        self.position_items(labyrinth)
        Items.LIST_OF_ITEMS.append(self)

    """ function used to position the items on their squares randomly """
    def position_items(self, labyrinth):
        self.coordinates = random.choice(labyrinth.void)
        labyrinth.void.remove(self.coordinates)



