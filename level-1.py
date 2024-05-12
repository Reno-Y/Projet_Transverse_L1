from function import parallax
import pygame
from function import parallax
from Class import Animation
from pause import pause_menu
from player import Player


width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

moving_right = False
moving_left = False
player = Player(width / 4, height / 1.8, screen, 2)
player_idle = Animation(screen, width, height, 'Assets/character/player/idle.png', 2.4, 128, 128,
                        player.pos)
player_run = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                       player.pos)
player.level = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
scroll = 0
inf = 0
while True:
    screen.fill((0, 0, 0))

    inf += 1
    parallax(inf, scroll, "assets/background/level1")
    scroll += 0
    if player.pos_y > height / 1.8:
        player.strength(0, 40)
    else:
        player.pos_y = height / 1.8
        player.speed_y = 0

    if moving_right:

        player_run.draw()
        player.strength(player.walk_speed, 0)
        player_run.update()
        scroll += 4
    if moving_left:
        player_run.draw()
        player.strength(player.walk_speed, 0)
        player_run.update()
        scroll += -4
    elif not moving_right and not moving_left:
        player_idle.draw()
        player_idle.update()

    player.mouvement()

    if player.pos_x > width:
        player.pos_x = 0
    if player.pos_x < 0:
        player.pos_x = width

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_LEFT:
                moving_left = True
        if event.type == pygame.KEYUP:
            player.strength(0, 100)
            player.can_move = False
            if event.key == pygame.K_ESCAPE:
                pause_menu(True)


    pygame.display.flip()
    pygame.time.Clock().tick(60)

    # to do: faut faire la map pour l'incorporer dans les colision car on est hors de de la range sinon changer de
    # méthode.