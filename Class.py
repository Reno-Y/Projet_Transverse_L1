import pygame


class Startup:
    pygame.mixer.init()
    studio_logo = pygame.image.load("Assets/menu/Shinobi_studio.png")
    studio_sound = pygame.mixer.Sound("sound/music/startup.mp3")
