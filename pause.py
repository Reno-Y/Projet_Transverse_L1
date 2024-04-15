import pygame
from Class import Button

width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
button_width, button_height = start_button.get_rect().width, start_button.get_rect().height
pause = pygame.rect.Rect((width / 4, height / 4, (width / 4) * 2, (height / 4) * 2))

resume_button = pygame.image.load('Assets/menu/resume/resume1.png').convert_alpha()
resume_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 - button_height * 3.5 / 2),
                       resume_button, 3.5, screen, 'Assets/menu/resume/resume_spritesheet.png', width, height)

quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
quit_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + (button_height * 3.5 / 2) * 3),
                     quit_button,
                     3.5, screen, 'Assets/menu/quit/quit_spritesheet.png', width, height)
setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
setting_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + button_height * 3.5 / 2),
                        setting_button,
                        3.5, screen, 'Assets/menu/settings/settings_spritesheet.png', width, height)
transparency = pygame.Surface((width, height), pygame.SRCALPHA)


# on définit un rectangle pour le menu pause
def draw_screen():
    pygame.draw.rect(transparency, (0, 0, 0, 100), [0, 0, width, height])


def pause_menu(state):
    draw_screen()
    pygame.draw.rect(screen, (0, 0, 0), pause)
    paused = state
    screen.blit(transparency, (0, 0))

    while paused:
        quit_button.draw()
        setting_button.draw()
        resume_button.draw()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
            if quit_button.clicked():
                quit()
            if resume_button.clicked():
                paused = False

        pygame.display.update()
        pygame.display.flip()
        pygame.time.Clock().tick(60)
        # on affiche le menu pause
