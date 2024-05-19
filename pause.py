import pygame
from button import Button
from main_menu import run_menu
from function import parallax, parallax_init

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
button_width, button_height = start_button.get_rect().width, start_button.get_rect().height
clock = pygame.time.Clock()

resume_button = pygame.image.load('Assets/menu/resume/resume1.png').convert_alpha()
resume_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 - (button_height * 3.5) * 1.5),
                       resume_button, 3.5, screen, 'Assets/menu/resume/resume_spritesheet.png', width, height)

quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
quit_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + (button_height * 3.5 / 2) * 3),
                     quit_button,
                     3.5, screen, 'Assets/menu/quit/quit_spritesheet.png', width, height)
setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
setting_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + button_height * 3.5 / 2),
                        setting_button,
                        3.5, screen, 'Assets/menu/settings/settings_spritesheet.png', width, height)
main_menu_button = pygame.image.load('Assets/menu/main_menu/main_menu_1.png').convert_alpha()
main_menu_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 - button_height * 3.5 / 2),
                          main_menu_button,
                          3.5, screen, 'Assets/menu/main_menu/main_menu_spritesheet.png', width, height)
transparency = pygame.Surface((width, height), pygame.SRCALPHA)

screen = pygame.display.set_mode((width, height))
inf = 0
scroll = 0


def run_pause_menu(boolean):
    pygame.draw.rect(transparency, (0, 0, 0, 100), [0, 0, width, height])
    screen.blit(transparency, (0, 0))
    run = boolean
    bg_images = parallax_init("assets/background/sunset_sky")
    scroll = 0

    while run:
        screen.fill((0, 0, 0))  # remplissage de l'écran
        parallax(scroll, bg_images, screen)
        scroll += 2

        quit_button.draw()
        setting_button.draw()
        resume_button.draw()
        main_menu_button.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

            if quit_button.clicked():
                quit()

            if resume_button.clicked():
                run = False

            if main_menu_button.clicked():
                run_menu(True)
                run = False

        clock.tick(60)
        pygame.display.update()
