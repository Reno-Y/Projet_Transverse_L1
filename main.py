import pygame
from Class import *

pygame.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height-60))
pygame.display.set_caption('Iron Lung')
# récupère la taille de l'écran et affiche une fenêtre
clock = pygame.time.Clock()


run = True
while run :

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60) #limite les fps à 60
pygame.quit()
