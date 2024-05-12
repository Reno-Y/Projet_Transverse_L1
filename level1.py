import pygame
from function import parallax
from Class import Animation
from pause import run_pause_menu

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))


player_location = [width / 4, height / 1.8]
player_idle = Animation(screen, width, height, 'Assets/character/player/idle.png', 2.4, 128, 128,
                        player_location)
player_run = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                       player_location)


def run_level1(boolean):

    moving_right = False
    moving_left = False
    scroll = 0
    inf = 0

    while boolean:
        screen.fill((0, 0, 0))

        inf += 1
        parallax(inf, scroll, "assets/background/level1")
        scroll += 0

        if moving_right:
            player_run.draw()
            player_location[0] += 20
            player_run.update()
            scroll += 4
        if moving_left:
            player_run.draw()
            player_location[0] -= 20
            player_run.update()
            scroll += -4
        elif not moving_right and not moving_left:
            player_idle.draw()
            player_idle.update()

        if player_location[0] > width:
            player_location[0] = 0
        if player_location[0] < 0:
            player_location[0] = width

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    moving_right = True
                if event.key == pygame.K_LEFT:
                    moving_left = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    moving_right = False
                if event.key == pygame.K_LEFT:
                    moving_left = False
                if event.key == pygame.K_ESCAPE:
                    run_pause_menu(True)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
