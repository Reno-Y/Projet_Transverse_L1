from function import background_apparition, parallax, parallax_init
from music import Music
from dialogue import Dialogue
import pygame
from level1 import run_level1

#il faut changer l'instance

#TODO changer les texte pour un tuto
pygame.init()
pygame.mixer.init()
pygame.font.init()  # initialisation de pygame
title_font = pygame.font.Font('Assets/font/hero-speak.ttf', 60)  # police d'écriture
clock = pygame.time.Clock()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h  # récupération de la taille de l'écran
screen = pygame.display.set_mode((width, height))  # initialisation de la fenêtre

text = ["HARU : C'EST DONC LA FIN ?",
        "             EST CE QUE TOUT CELA EN VALAIT VRAIMENT LE COUP ?",
        "             CE VOYAGE TOUCHE PEUT ETRE A SA FIN MAIS CE N'EST QUE LE DEBUT D'UNE NOUVELLE AVENTURE",
        "             JE SUIS PRET A AFFRONTER TOUT CE QUI M'ATTEND",
        "             ET VOUS ?"]

text2 = ["HARU : SUITE DU TEXTE T'AS CAPTE ?",
         "             J'SUIS PAS ASSEZ PAYE POUR ECRIRE TOUT CA",
         "             HELPPPPPP"]

dialogue = Dialogue(screen, height, width, width / 1.2, height / 4, width / 2 - width / 2.4,
                    height / 4 + (7 * height / 16), text,
                    (255, 255, 255))
dialogue2 = Dialogue(screen, height, width, width / 1.2, height / 4, width / 2 - width / 2.4,
                     height / 4 + (7 * height / 16), text2,
                     (255, 255, 255))


def run_ending(boolean):
    music = Music("sound/music/ending.mp3")
    background_apparition('Assets/background/sunset_sky.png')  # fade in de l'image de fond
    music.play(-1)  # lancement de la musique
    scroll = 0
    run = boolean
    bg_images = parallax_init("assets/background/sunset_sky")
    while run:

        screen.fill((0, 0, 0))  # remplissage de l'écran
        parallax(scroll, bg_images, screen)
        scroll += 2

        dialogue.draw()  # affichage du dialogue

        if dialogue.closed():  # si le dialogue est fermé
            dialogue2.draw()  # affichage du deuxième dialogue

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogue.skip()  # passage au dialogue suivant
                    dialogue.next()  # affichage du dialogue suivant
                    dialogue2.next()
                    dialogue2.closed()
                    dialogue.closed()
                    if dialogue2.closed():

                        run_level1(True)
                        run_ending(False)

                if event.key == pygame.K_ESCAPE:
                    run = False
                if event.key == pygame.K_RETURN:
                    dialogue.draw()
        clock.tick(60)
        pygame.display.update()
    pygame.quit()
