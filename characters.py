import pygame
from pygame.locals import *

""" 

Class that allows us to instanciate the chatacters 

"""
class Characters:
    """ constructor of the character """

    def __init__(self, pictures_path, coordinates):
        self.head = pygame.image.load(pictures_path).convert_alpha()
        self.coordinates = coordinates

""" Class of the boss """
class Boss(Characters):
    """ constructor of the boss """
    def __init__(self, image_path, coordinates):
        """ We instanciate a character because a Boss is a Character """
        Characters.__init__(self, image_path, coordinates)

    """ Function to loose(MacGyver dies) if we don't have the serynge """
    def lose(self, macgyver, dead_path):
        macgyver.head = pygame.image.load(dead_path).convert_alpha()


"""
  
 Class of the character. The player and the guardian are the characters.
   
"""
class Player(Characters):
    """ Constructor of the character """
    def __init__(self, image_path, coordinates):
        Characters.__init__(self, image_path, coordinates)
        """ number of items picked up by MacGyver """
        self.count = 0
        """ Flag that becomes True if we win """
        self.victorious = False

    """ Allows the player to move from a square to another one """
    def move(self, event):
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

    """ Getting rid of the boss """
    def neutralize(self, labyrinth, the_boss, arrival_coordinates):
        labyrinth.void.append(the_boss.coordinates)
        labyrinth.void.append(arrival_coordinates)
