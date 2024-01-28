import pygame
from Class import Startup, GameInfo

pygame.init()
pygame.mixer.init()

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height - 60))
clock = pygame.time.Clock()  # horloge pour limiter les fps

GameInfo()
Startup(width, height)

run = True
while run:  # boucle principale

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    clock.tick(60)  # limite les fps à 60
pygame.quit()
