import pygame
import os

pygame.init()
pygame.mixer.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

player_idle_sheet = pygame.image.load('Assets/character/player/idle.png').convert_alpha()


class SpriteSheet:
    def __init__(self, image):
        self.sheet = image

    def get(self, frame, image_width, image_height, scale):
        image = pygame.Surface((image_width, image_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * image_width, 0, image_width, image_height))
        image = pygame.transform.scale(image, (image_width * scale, image_height * scale))
        image.set_colorkey((0, 0, 0))
        return image

