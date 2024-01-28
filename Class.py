import pygame
import os

pygame.init()
pygame.mixer.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

player_idle_sheet = pygame.image.load('Assets/character/player/idle.png').convert_alpha()


class Spritesheet:
    def __init__(self, filename):
        self.sheet = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite


class Parallax:
    def __init__(self, folder):
        self.folder = folder
        self.images = []

    def import_parallax(self, folder):

        for file in os.listdir(folder):
            self.images.append(pygame.image.load(os.path.join(folder, file)).convert_alpha())

    def draw_bg(self):
        for image in self.images:
            screen.blit(image, (0, 0))
