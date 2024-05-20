import pygame
import pytmx
from pygame import surface

from bullet import Bullet
from function import *
from player2 import Player
from tiles_map import *
from pause_menu import PauseMenu
from button import Button

from animation import Animation
from dialogue import Dialogue

pygame.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
MAP_COLLISION_LAYER = 0


class TittleName:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        title_image = pygame.image.load('Assets/menu/Chronicles_of_Etheria.png').convert_alpha()
        self.title_image = pygame.transform.scale(title_image, (self.width, self.height))
        # on charge l'image du titre et on la redimensionne

    def draw(self):
        self.screen.blit(self.title_image, (0, 0))
        # on affiche l'image du titre


# -------------------------------------------------------------------#


class Game(object):
    def __init__(self, list_player_pos, level_directory):
        # Set up a level to load
        self.scroll = 310
        self.bg_images = parallax_init("assets/background/level0")
        self.currentLvNb = 0
        self.pause = PauseMenu(screen)
        self.levels = load_levels(level_directory)
        self.currentLevel = self.levels[self.currentLvNb]
        self.move = False
        # Create a player object and set the level it is in
        self.player = Player(list_player_pos[self.currentLvNb])
        self.player.currentLevel = self.currentLevel
        self.bullets = pygame.sprite.Group()
        Bullet.player = self.player
        self.move_left = False
        self.move_right = False

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Get keyboard input and move player accordingly
            elif pygame.mouse.get_pressed()[0]:
                bullet = self.player.shoot(screen, pygame.mouse.get_pos())
                if bullet is not None:
                    self.bullets.add(bullet)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause.run(True):
                        return "main_menu"
                elif event.key == pygame.K_LEFT:
                    self.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.move_right = True
                elif event.key == pygame.K_UP:
                    self.player.jump()
                elif event.key == pygame.K_w:
                    self.player.dash()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_left = False
                if event.key == pygame.K_RIGHT:
                    self.move_right = False

        if not self.move_right and not self.move_left:
            self.player.stop()
        else:
            if self.move_left:
                self.player.goLeft()
            if self.move_right:
                self.player.goRight()

        if self.player.rect.x > SCREEN_WIDTH:
            if len(self.levels) > self.currentLvNb:
                self.currentLvNb += 1
                self.currentLevel = self.levels[self.currentLvNb]
            else:
                return False
        if self.player.rect.y > SCREEN_HEIGHT:
            return "main_menu"

        return True

    def runLogic(self):
        # Update player movement and collision logic
        self.player.update()
        self.bullets.update()
        self.scroll += 2 - self.player.difference

    # Draw level, player, overlay

    def draw(self, screen):
        screen.fill((135, 206, 235))
        parallax(self.scroll, self.bg_images, screen)
        self.currentLevel.draw(screen)
        self.bullets.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()


def load_levels(levels_directory):
    levels = []
    for file_name in os.listdir(levels_directory):
        if file_name.endswith(".tmx"):
            level_path = os.path.join(levels_directory, file_name)
            levels.append(Level(fileName=level_path))
    return levels
