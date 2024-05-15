import pygame
from function import parallax
from Class import Animation
from pause import run_pause_menu
from player import Player

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))


player_location = [width / 4, height / 1.8]
player_idle = Animation(screen, width, height, 'Assets/character/player/idle.png', 2.4, 128, 128,
                        player_location)
player_run = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                       player_location)
Player = Player()

def run_level1(boolean):


    scroll = 0
    inf = 0

    while boolean:
        screen.fill((0, 0, 0))

        inf += 1
        parallax(inf, scroll, "assets/background/level1")
        scroll += 0

        Player.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(60)
