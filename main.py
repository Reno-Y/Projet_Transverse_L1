import pygame
from function import Startup, GameInfo, Menu
from Class import Spritesheet

TILE_SIZE = 32  # Résolution des textures

# initialisation de pygame et de la clock
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# récupération de la taille de l'écran ainsi que l'initialisation de la fenêtre
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

GameInfo()  # logo et titre du jeu
Startup()  # écran de démarrage
Menu("Assets/background/summer")

