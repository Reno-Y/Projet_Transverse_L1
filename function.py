import pygame
import time

pygame.init()
pygame.mixer.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
pygame.font.init()
font = pygame.font.Font('Assets/font/hero-speak.ttf', 85)


def GameInfo():
    """
    Logo et titre du jeu
    :return:
    """
    pygame.display.set_caption('Iron Lung')
    game_icon = pygame.image.load('Assets/menu/Shinobi_studio.png')
    pygame.display.set_icon(game_icon)


def Startup():
    startup_logo = pygame.image.load('Assets/menu/Shinobi_studio.png')  # image de démarrage
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


def Menu():
    background = pygame.image.load('Assets/background/summer/summer.png')
    background = pygame.transform.scale(background, (width, height))
    menu_music = pygame.mixer.Sound("sound/music/theme_of_love.mp3")
    menu_music.play(-1)

    for i in range(255):  # fait apparaitre l'image
        screen.fill((0, 0, 0))
        background.set_alpha(i)
        screen.blit(background, (0, 0))
        pygame.display.update()
        time.sleep(0.000001)

    run = True
    while run:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


def Game(clock):
    run = True
    while run:  # boucle principale
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)  # limite les fps à 60
    pygame.quit()


def dialogue(text):
    snip = font.render('', False, (255, 255, 255))
    text = 'Iron Lung'
    timer = pygame.time.Clock()
    counter = 0
    speed = 3
    done = False
