import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BUTTON_SCALE
from function import parallax, parallax_init


class PauseMenu:

    def __init__(self, screen):

        from button import Button
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = screen
        self.start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
        self.button_width, self.button_height = self.start_button.get_rect().width, self.start_button.get_rect().height
        self.scale = self.width // (self.button_width * (1 / BUTTON_SCALE))
        self.clock = pygame.time.Clock()

        self.resume_button = pygame.image.load('Assets/menu/resume/resume1.png').convert_alpha()
        self.resume_button = Button((SCREEN_WIDTH / 2 - self.button_width * self.scale / 2), (SCREEN_HEIGHT / 2 - (self.button_height * self.scale) * 1.5),
                                    self.resume_button, self.scale, self.screen, 'Assets/menu/resume/resume_spritesheet.png', SCREEN_WIDTH,
                                    SCREEN_HEIGHT)

        self.quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
        self.quit_button = Button((SCREEN_WIDTH / 2 - self.button_width * self.scale / 2), (SCREEN_HEIGHT / 2 + (self.button_height * self.scale / 2) * 3),
                                  self.quit_button,
                                  self.scale, self.screen, 'Assets/menu/quit/quit_spritesheet.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
        self.setting_button = Button((SCREEN_WIDTH / 2 - self.button_width * self.scale / 2), (SCREEN_HEIGHT / 2 + self.button_height * self.scale / 2),
                                     self.setting_button,
                                     self.scale, self.screen, 'Assets/menu/settings/settings_spritesheet.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.main_menu_button = pygame.image.load('Assets/menu/main_menu/main_menu_1.png').convert_alpha()
        self.main_menu_button = Button((SCREEN_WIDTH / 2 - self.button_width * self.scale / 2), (SCREEN_HEIGHT / 2 - self.button_height * self.scale / 2),
                                       self.main_menu_button,
                                       self.scale, self.screen, 'Assets/menu/main_menu/main_menu_spritesheet.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.scroll = 0

    def run(self, boolean):

        run = boolean
        scroll = 0
        bg_images = parallax_init("assets/background/sunset_sky")
        while run:
            self.screen.fill((0, 0, 0))  # remplissage de l'écran
            parallax(scroll, bg_images, self.screen)
            scroll += 2

            self.quit_button.draw()
            self.setting_button.draw()
            self.resume_button.draw()
            self.main_menu_button.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                elif self.quit_button.clicked():
                    quit()

                elif self.resume_button.clicked():
                    run = False

                elif self.main_menu_button.clicked():
                    # run_menu(True)
                    run = False
                    return True

            self.clock.tick(FPS)
            pygame.display.update()