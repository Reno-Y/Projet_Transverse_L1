import pygame

pygame.init()
pygame.mixer.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

player_idle_sheet = pygame.image.load('Assets/character/player/idle.png')
