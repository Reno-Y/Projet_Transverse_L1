import pygame
from function import parallax
from Class import Animation, Game
from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

width, height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((width, height))


player_location = [width / 4, height / 1.8]
player_idle = Animation(screen, width, height, 'Assets/character/player/idle.png', 2.4, 128, 128,
                        player_location)
player_run = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                       player_location)

def run_level1(boolean):


    scroll = 0

    game = Game()
    while boolean:

        boolean = game.processEvents()
        game.runLogic()
        game.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
