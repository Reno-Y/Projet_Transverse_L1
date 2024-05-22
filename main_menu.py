from function import background_apparition, parallax, parallax_init
from music import Music
import pygame
from cinematic import run_ending, run_win
from animation import Animation
from button import Button
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SCALE
from level import run_level1
from title_name import TitleName
pygame.init()
pygame.mixer.init()
pygame.font.init()  # initialisation de pygame

title_font = pygame.font.Font('Assets/font/hero-speak.ttf', 60)  # police d'écriture
clock = pygame.time.Clock()
width, height = SCREEN_WIDTH, SCREEN_HEIGHT  # Récupération de la taille de l'écran
screen = pygame.display.set_mode((width, height))  # Initialisation de la fenêtre

player_walk = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                        ((width / 4) - 300, height - (height / 1.95)))

princess_walk = Animation(screen, width, height, 'Assets/character/hime/walk.png', 2, 128, 128,
                          (width - (width / 4), height - (height / 2.2)))

start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()

button_width, button_height = start_button.get_rect().width, start_button.get_rect().height
scale = width // (button_width * (1 / BUTTON_SCALE))

start_button = Button((width / 2 - button_width * scale / 2),
                      (height / 2 - (button_height * scale) * 0.5), start_button, scale, screen,
                      'Assets/menu/start/start_spritesheet.png', width, height)

setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
setting_button = Button((width / 2 - button_width * scale / 2), (height / 2 + (button_height * scale) / 2),
                        setting_button,
                        scale, screen, 'Assets/menu/settings/settings_spritesheet.png', width, height)

quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
quit_button = Button((width / 2 - button_width * scale / 2), (height / 2 + (button_height * scale / 2) * 3),
                     quit_button,
                     scale, screen, 'Assets/menu/quit/quit_spritesheet.png', width, height)

title_name = TitleName(screen, width, height)


def run_menu(boolean):
    background_apparition('Assets/menu/menu.png')

    menu_music = Music("sound/music/theme_of_love.mp3")
    menu_music.play(-1)
    scroll = 0
    run = boolean
    bg_images = parallax_init("assets/background/summer")
    while run:

        screen.fill((0, 0, 0))
        parallax(scroll, bg_images, screen)
        scroll += 2
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
                if run_ending(True) == "main_menu":
                    break
                if run_level1(True) == "main_menu":
                    break
                if run_ending(True) == "main_menu":
                    break
                if run_win(True) == "main_menu":
                    break

            if quit_button.clicked():
                run = False
                menu_music.soundtrack.stop()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.QUIT:
                run = False
        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()
