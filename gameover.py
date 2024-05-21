import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BUTTON_SCALE
from animation import Animation


class GameOver:

    def __init__(self, screen):

        from button import Button
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = screen
        self.start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
        self.button_width, self.button_height = self.start_button.get_rect().width, self.start_button.get_rect().height

        self.scale = self.width // (self.button_width * (1 / BUTTON_SCALE))
        self.clock = pygame.time.Clock()

        self.main_menu_button = pygame.image.load('Assets/menu/main_menu/main_menu_1.png').convert_alpha()
        self.main_menu_button = Button((SCREEN_WIDTH / 2 - self.button_width * self.scale / 2),
                                       (SCREEN_HEIGHT / 2 + 8 * (self.button_height * self.scale / 2)),
                                       self.main_menu_button,
                                       self.scale, self.screen, 'Assets/menu/main_menu/main_menu_spritesheet.png',
                                       SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player_death = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                      'Assets/character/player/Dead2.png', 3.5,
                                      128, 128,
                                      (((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 7)),
                                       ((SCREEN_HEIGHT / 4) - (SCREEN_HEIGHT / 7))))
        gameover_image = pygame.image.load('Assets/background/gameover/gameover.png')
        self.gameover_image = pygame.transform.scale(gameover_image, (self.width, self.height))

    def run(self, boolean):

        run = boolean

        while run:
            self.screen.fill((0, 0, 0))  # remplissage de l'écran
            self.screen.blit(self.gameover_image, (0, 0))

            self.player_death.draw()
            self.player_death.play_once(300)

            self.main_menu_button.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                elif self.main_menu_button.clicked():
                    return True

            self.clock.tick(FPS)
            pygame.display.update()
