import pygame
from function import launch_logo, game_window_info
from main_menu import run_menu

# initialisation de pygame et de la clock
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# récupération de la taille de l'écran ainsi que l'initialisation de la fenêtre
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))


game_window_info()  # logo et titre du jeu
launch_logo()  # logo de démarrage
run_menu(True)


