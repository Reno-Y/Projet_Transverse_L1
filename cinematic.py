from function import background_apparition, parallax, parallax_init
from music import Music
from dialogue import Dialogue
from animation import Animation
from button import Button
import pygame
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, BUTTON_SCALE
from pause_menu import PauseMenu
from title_name import Title

#  Il faut changer l'instance

#  TODO changer les texte pour un tuto
pygame.init()
pygame.mixer.init()
pygame.font.init()  # Initialisation de pygame
title_font = pygame.font.Font('Assets/font/hero-speak.ttf', 60)  # Police d'écriture
clock = pygame.time.Clock()
width, height = SCREEN_WIDTH, SCREEN_HEIGHT  # Récupération de la taille de l'écran
screen = pygame.display.set_mode((width, height))  # Initialisation de la fenêtre


def run_ending(boolean):
    text = ["HARU : C'EST DONC LA FIN ?",
            "             EST CE QUE TOUT CELA EN VALAIT VRAIMENT LA PEINE ?",
            "             CE VOYAGE TOUCHE PEUT ETRE A SA FIN MAIS CE N'EST QUE LE DEBUT D'UNE NOUVELLE AVENTURE",
            "             JE SUIS PRET A AFFRONTER TOUT CE QUI M'ATTEND",
            "             ET VOUS ?"]

    text2 = ["HARU : PARFOIS JE ME RAPELLE DE CE PARCHEMIN QUE J'AIS TROUVE DANS LA CAVE DE MON GRAND PERE",
             "             IL PARLAIT D'UTILISER LES FLECHES DIRECTIONNELLES POUR SE DEPLACER ET DE CLIQUER GAUCHE POUR TIRER",
             "             ON POUVAIT MEME EFFECTUER UN DASH EN APPUYANT SUR W",
             "             MAIS SURTOUT IL FAUT TUER TOUTES LES GEMMES POUR POUVOIR AVANCER"]

    dialogue = Dialogue(screen, height, width, width / 1.2, height / 4, width / 2 - width / 2.4,
                        height / 4 + (7 * height / 16), text,
                        (255, 255, 255))
    dialogue2 = Dialogue(screen, height, width, width / 1.2, height / 4, width / 2 - width / 2.4,
                         height / 4 + (7 * height / 16), text2,
                         (255, 255, 255))

    music = Music("sound/music/ending.mp3")
    background_apparition('Assets/background/sunset_sky.png')  # Fondu entrant de l'image de fond
    music.play(-1)  # Lancement de la musique
    scroll = 0
    pause = PauseMenu(screen)
    run = boolean
    bg_images = parallax_init("assets/background/sunset_sky")

    while run:

        screen.fill((0, 0, 0))  # Remplissage de l'écran
        parallax(scroll, bg_images, screen)
        scroll += 1

        dialogue.draw()  # Affichage du dialogue

        if dialogue.closed():  # Si le dialogue est fermé
            dialogue2.draw()  # Affichage du deuxième dialogue

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogue.skip()  # Passage au dialogue suivant
                    dialogue.next()  # Affichage du dialogue suivant
                    dialogue2.next()
                    dialogue2.closed()
                    dialogue.closed()
                    if dialogue2.closed():
                        run = False

                if event.key == pygame.K_ESCAPE:
                    if pause.run(True):
                        music.soundtrack.stop()
                        return "main_menu"

                if event.key == pygame.K_RETURN:
                    dialogue.draw()
        clock.tick(FPS)
        pygame.display.update()
    music.soundtrack.stop()
    return run


def run_win(boolean):
    pause = PauseMenu(screen)
    start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
    button_width, button_height = start_button.get_rect().width, start_button.get_rect().height

    scale = width // (button_width * (1 / BUTTON_SCALE))

    main_menu_button = pygame.image.load('Assets/menu/main_menu/main_menu_1.png').convert_alpha()
    main_menu_button = Button((SCREEN_WIDTH / 2 - button_width * scale / 2), (SCREEN_HEIGHT / 2),
                              main_menu_button,
                              scale, screen, 'Assets/menu/main_menu/main_menu_spritesheet.png',
                              SCREEN_WIDTH, SCREEN_HEIGHT)
    player_idle = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'Assets/character/player/Idle.png', 3, 128,
                            128,
                            (((SCREEN_WIDTH / 2) - (SCREEN_WIDTH / 4)),
                             ((SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 9))))
    hime_idle = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'Assets/character/hime/idle.png', 2.7, 128, 128,
                          (((SCREEN_WIDTH / 2) + (SCREEN_WIDTH / 16)),
                           ((SCREEN_HEIGHT / 2) + (SCREEN_HEIGHT / 7))))

    scroll = 0
    music = Music("sound/music/theme_of_love.mp3")
    bg_images = parallax_init("assets/background/beach")
    run = boolean
    win = Title(screen, SCREEN_WIDTH, SCREEN_HEIGHT, 'Assets/menu/win.png')
    music.play(-1)
    while run:

        screen.fill((0, 0, 0))  # remplissage de l'écran
        parallax(scroll, bg_images, screen)
        scroll += 0.5
        player_idle.draw()
        player_idle.update()
        hime_idle.draw(orientation=True)
        hime_idle.update()
        win.draw()

        main_menu_button.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_ESCAPE:
                    if pause.run(True) == "main_menu":
                        music.soundtrack.stop()
                        return "main_menu"

            elif main_menu_button.clicked():

                music.soundtrack.stop()
                return "main_menu"

        clock.tick(FPS)
        pygame.display.update()
    return False
