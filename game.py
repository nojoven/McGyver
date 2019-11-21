from time import sleep
import pygame
from pygame.locals import *
from constants import *
from labyrinth import Labyrinth
from characters import Boss, Player
from item import Items

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
def display_items(item):
    square_window.blit(item.image, item.coordinates)

"""Display Characters"""
def display_character(character):
    square_window.blit(character.head, character.coordinates)

""" Loop of the game """
while IS_RUNNING:

    """ Displays the game """
    level_components.display_labyrinth(square_window)
    display_character(mac)
    display_character(gatekeeper)
    for item in Items.LIST_OF_ITEMS:
        display_items(item)
    pygame.display.flip()

    """ What happens when we meet the gatekeeper """
    if mac.coordinates in FIGHT_POSITION:
        if mac.count == 3:
            mac.neutralize(level_components, gatekeeper, EXIT_POSITION)
        else:
            gatekeeper.lose(mac, CARCASS)
            square_window.blit(mac.head, mac.coordinates)
            IS_RUNNING = False

    """ Reaching the exit position """
    if mac.coordinates == EXIT_POSITION:
        mac.victorious = True
        IS_RUNNING = False

    """ Events detection """
    for event in pygame.event.get():
        if event.type == QUIT:
            IS_RUNNING = False
        if event.type == KEYDOWN:
            x, y = mac.move(event)

            """ Square where we can walk, or with a serynge component, or wall so we can't use it"""
            if (x, y) in level_components.void:
                level_components.void.remove((x, y))
                moving = True

            elif (x, y) in [item.coordinates for item in Items.LIST_OF_ITEMS]:
                mac.count += 1
                Items.LIST_OF_ITEMS = [item for item in Items.LIST_OF_ITEMS if item.coordinates != (x, y)]
                moving = True

            else:
                moving = False

            """ Moving """
            if moving == True:
                level_components.void.append(mac.coordinates)
                mac.coordinates = (x, y)

""" Outcome """
if mac.victorious == True:
    path = VICTORY
else:
    path = FAILURE

""" Showing the outcome notification """
notification = pygame.image.load(path).convert()
square_window.blit(notification, (100, 300))
pygame.display.flip()

""" Waiting 1 seconds before closing the window """
sleep(1)

