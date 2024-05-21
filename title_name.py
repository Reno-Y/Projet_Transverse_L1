import pygame
from music import Music
pygame.init()


class TitleName:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        title_image = pygame.image.load('Assets/menu/Chronicles_of_Etheria.png').convert_alpha()
        self.title_image = pygame.transform.scale(title_image, (self.width, self.height))
        # on charge l'image du titre et on la redimensionne
        self.music = Music("sound/music/voyage.mp3")

    def draw(self):
        self.screen.blit(self.title_image, (0, 0))
        # Affiche l'image du titre


class Title:
    def __init__(self, screen, width, height, image_path):
        self.screen = screen
        self.width = width
        self.height = height
        title_image = pygame.image.load(image_path).convert_alpha()
        self.title_image = pygame.transform.scale(title_image, (self.width, self.height))

    def draw(self):
        self.screen.blit(self.title_image, (0, 0))
        # Affiche l'image du titre
