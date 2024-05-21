import time

import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BUTTON_SCALE
from animation import Animation
from function import parallax, parallax_init
from music import Music
from pause_menu import PauseMenu

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Win:

    def __init__(self, screen):

        from button import Button
        self.pause = PauseMenu(screen)
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = screen
        self.start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
        self.button_width, self.button_height = self.start_button.get_rect().width, self.start_button.get_rect().height

        self.scale = self.width // (self.button_width * (1 / BUTTON_SCALE))
        self.clock = pygame.time.Clock()

        self.main_menu_button = pygame.image.load('Assets/menu/main_menu/main_menu_1.png').convert_alpha()
        self.main_menu_button = Button((SCREEN_WIDTH / 2 - self.button_width * self.scale / 2), (SCREEN_HEIGHT / 2),
                                       self.main_menu_button,
                                       self.scale, self.screen, 'Assets/menu/main_menu/main_menu_spritesheet.png',
                                       SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_idle = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'Assets/character/player/Idle.png', 3, 128,
                                     128,
                                     (((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)),
                                      ((SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 9))))
        self.hime_idle = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'Assets/character/hime/idle.png', 2.7, 128, 128,
                                   (((SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 16)),
                                    ((SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 7))))

    def run(self, boolean):
        scroll = 0
        music = Music("sound/music/theme_of_love.mp3")
        bg_images = parallax_init("assets/background/beach")
        run = boolean
        from Class import Title
        win = Title(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'Assets/menu/win.png')
        music.play(-1)
        while run:

            self.screen.fill((0, 0, 0))  # remplissage de l'écran
            parallax(scroll, bg_images, self.screen)
            scroll += 0.5
            self.player_idle.draw()
            self.player_idle.update()
            self.hime_idle.draw(orientation=True)
            self.hime_idle.update()
            win.draw()

            self.main_menu_button.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_ESCAPE:
                        if self.pause.run(True) == "main_menu":
                            music.soundtrack.stop()
                            return "main_menu"

                elif self.main_menu_button.clicked():

                    music.soundtrack.stop()
                    run = False
                    return "main_menu"

            self.clock.tick(FPS)
            pygame.display.update()
        return False

