from function import background_apparition, parallax
from Class import Animation, Button, Music, TittleName
import pygame
from ending import run_ending

pygame.init()
pygame.mixer.init()
pygame.font.init()  # initialisation de pygame
title_font = pygame.font.Font('Assets/font/hero-speak.ttf', 60)  # police d'écriture
clock = pygame.time.Clock()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h  # récupération de la taille de l'écran
screen = pygame.display.set_mode((width, height))  # initialisation de la fenêtre

player_walk = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                        ((width / 4) - 300, height - (height / 1.95)))

princess_walk = Animation(screen, width, height, 'Assets/character/hime/walk.png', 2, 128, 128,
                          (width - (width / 4), height - (height / 2.2)))

start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
button_width, button_height = start_button.get_rect().width, start_button.get_rect().height

start_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 - button_height * 3.5 / 2),
                      start_button, 3.5, screen, 'Assets/menu/start/start_spritesheet.png', width, height)

setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
setting_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + button_height * 3.5 / 2),
                        setting_button,
                        3.5, screen, 'Assets/menu/settings/settings_spritesheet.png', width, height)

quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
quit_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + (button_height * 3.5 / 2) * 3),
                     quit_button,
                     3.5, screen, 'Assets/menu/quit/quit_spritesheet.png', width, height)

title_name = TittleName(screen, width, height)


def run_menu(boolean):
    background_apparition('Assets/menu/menu.png')

    menu_music = Music("sound/music/theme_of_love.mp3")
    menu_music.play(-1)
    scroll = 0
    inf = 0
    run = boolean

    while run:

        screen.fill((0, 0, 0))
        inf += 2
        parallax(inf, scroll, "assets/background/summer")
        scroll += 4
        title_name.draw()
        start_button.draw()
        player_walk.update()
        player_walk.draw()
        princess_walk.update()
        princess_walk.draw()
        quit_button.draw()
        setting_button.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if start_button.clicked():
                menu_music.soundtrack.stop()
                run_ending(True)
                run = False

            if quit_button.clicked():
                run = False
                menu_music.soundtrack.stop()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)
        pygame.display.update()
    pygame.quit()
