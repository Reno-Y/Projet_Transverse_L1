import pygame
from function import lunch_logo, game_window_info, main_menu
from Class import SpriteSheet

TILE_SIZE = 32  # Résolution des textures

# initialisation de pygame et de la clock
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# récupération de la taille de l'écran ainsi que l'initialisation de la fenêtre
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))


game_window_info()  # logo et titre du jeu
lunch_logo()  # écran de démarrage

main_menu("Assets/background/summer")

