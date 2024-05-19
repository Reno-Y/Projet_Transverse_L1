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
    def __init__(self):
        # Set up a level to load
        self.scroll = 0
        self.bg_images = parallax_init("assets/background/level0")
        self.currentLevelNumber = 0
        self.pause = PauseMenu(screen)
        self.levels = []
        self.levels.append(Level(fileName="Assets/levels/level1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]
        self.move = False
        # Create a player object and set the level it is in
        self.player = Player(x=200, y=100)
        self.player.currentLevel = self.currentLevel
        self.bullets = pygame.sprite.Group()

    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Get keyboard input and move player accordingly
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause.run(True):
                        return False
                elif event.key == pygame.K_LEFT:
                    self.move = True
                    self.player.goLeft()
                elif event.key == pygame.K_RIGHT:
                    self.move = True
                    self.player.goRight()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) and self.player.changeX < 0:
                    self.move = False
                if (event.key == pygame.K_RIGHT) and self.player.changeX > 0:
                    self.move = False
        if (self.move == False):
            self.player.stop()

        return True

    def runLogic(self):
        # Update player movement and collision logic
        self.player.update()

    # Draw level, player, overlay
    def draw(self, screen):
        screen.fill((135, 206, 235))
        parallax(self.scroll, self.bg_images, screen)
        self.scroll += 2
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()
