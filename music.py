import pygame


class Music:
    def __init__(self, music_location):
        self.soundtrack = pygame.mixer.Sound(music_location)

    def play(self, loop):
        self.soundtrack.play(loop)
    # on joue la musique en boucle