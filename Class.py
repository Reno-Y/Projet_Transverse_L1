import pygame
import time


def GameInfo():
    """
    Logo et titre du jeu
    :return:
    """
    pygame.display.set_caption('Iron Lung')
    game_icon = pygame.image.load('Assets/menu/Shinobi_studio.png')
    pygame.display.set_icon(game_icon)


def Startup(width, height):
    """

    :param width: prend en compte la largeur de l'écran
    :param height: prend en compte la hauteur de l'écran
    :return:
    """
    startup_logo = pygame.image.load('Assets/menu/Shinobi_studio.png')  # image de démarrage
    screen = pygame.display.set_mode((width, height - 60))  # -60 pour enlever la barre de tache
    logo_size = startup_logo.get_rect().size

    centered_logo = (width / 2 - logo_size[0] / 2, height / 2 - logo_size[1] / 2)  # centre l'image
    time.sleep(1)  # temps d'attente avant le démarrage

    startup_sound = pygame.mixer.Sound("sound/music/startup.mp3")  # son de démarrage
    startup_sound.play()

    for i in range(255):  # fait apparaitre l'image
        screen.fill((0, 0, 0))
        startup_logo.set_alpha(i)
        screen.blit(startup_logo, centered_logo)
        pygame.display.update()
        time.sleep(0.001)
    time.sleep(1.7)

    for i in range(255, 0, -1):  # fait disparaitre l'image
        screen.fill((0, 0, 0))
        startup_logo.set_alpha(i)
        screen.blit(startup_logo, centered_logo)
        pygame.display.update()
        time.sleep(0.001)

