import pygame
import time
import os
from Class import Animation, Button, Music, TittleName, Dialogue

pygame.init()
pygame.mixer.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
pygame.font.init()
title_font = pygame.font.Font('Assets/font/hero-speak.ttf', 60)
canvas = pygame.Surface((width, height))
clock = pygame.time.Clock()


def game_window_info():
    pygame.display.set_caption('Chronicles of Etheria')
    game_icon = pygame.image.load('Assets/menu/Shinobi_studio.png')
    pygame.display.set_icon(game_icon)
    # on définit le titre et l'icone de la fenêtre


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
    # on affiche du texte à l'écran


def launch_logo():
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
    time.sleep(1)

    for i in range(255, 0, -1):  # fait disparaitre l'image
        screen.fill((0, 0, 0))
        startup_logo.set_alpha(i)
        screen.blit(startup_logo, centered_logo)
        pygame.display.update()
        time.sleep(0.001)


def background_images_list(folder):
    bg_images = []
    for file in os.listdir(folder):
        bg_image = pygame.image.load(os.path.join(folder, file)).convert_alpha()
        bg_image = pygame.transform.scale(bg_image, (width, height))
        bg_images.append(bg_image)
    return bg_images
    # on récupère une liste d'images pour le parallax


def background_apparition(folder):
    background = pygame.image.load(folder)
    background = pygame.transform.scale(background, (width, height))

    for i in range(0, 256, 10):  # fait apparaitre l'image
        screen.fill((0, 0, 0))
        background.set_alpha(i)
        screen.blit(background, (0, 0))
        pygame.display.update()
    # on fait apparaitre l'image de fond


def parallax(inf, scroll, folder):
    bg_images = background_images_list(folder)
    image1 = bg_images[0]
    image1 = pygame.transform.scale(image1, (width, height))
    bg_width = image1.get_rect().width

    for i in range(inf):
        speed = 1
        for y in bg_images:
            screen.blit(y, ((i * bg_width) - scroll * speed, 0))
            speed += 1
    # on fait défiler les images de fond


def end(folder):
    menu_music = Music("sound/music/ending.mp3")
    menu_music.play(-1)
    scroll = 0
    inf = 0
    background_apparition('Assets/background/sunset_sky.png')

    text = ["HARU : C'EST DONC LA FIN ?",
            "             EST CE QUE TOUT CELA EN VALAIT VRAIMENT LE COUP ?",
            "             CE VOYAGE TOUCHE PEUT ETRE A SA FIN MAIS CE N'EST QUE LE DEBUT D'UNE NOUVELLE AVENTURE",
            "             JE SUIS PRET A AFFRONTER TOUT CE QUI M'ATTEND",
            "             ET VOUS ?"]

    dialogue = Dialogue(screen, height, width, width / 1.2, height / 4, width / 2 - width / 2.4,
                        height / 4 + (7 * height / 16), text,
                        (255, 255, 255))

    run = True
    while run:

        screen.fill((0, 0, 0))
        inf += 1
        parallax(inf, scroll, folder)
        scroll += 2

        dialogue.draw()

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dialogue.skip()
                    dialogue.next()
                    dialogue.close()
                if event.key == pygame.K_ESCAPE:
                    run = False

        clock.tick(60)
        pygame.display.update()
    pygame.quit()


def main_menu(folder):
    background_apparition('Assets/menu/menu.png')
    scroll = 0
    inf = 0
    menu_music = Music("sound/music/theme_of_love.mp3")

    player_walk = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                            ((width / 4) - 300, height - (height / 1.95)))

    princess_walk = Animation(screen, width, height, 'Assets/character/hime/walk.png', 2, 128, 128,
                              (width - (width / 4), height - (height / 2.2)))

    start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
    button_width, button_height = start_button.get_rect().width, start_button.get_rect().height

    start_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 - button_height * 3.5 / 2),
                          start_button, 3.5, screen, 'Assets/menu/start/start_spritesheet.png', width, height)

    setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
    setting_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + button_height * 3.5 / 2),
                            setting_button,
                            3.5, screen, 'Assets/menu/settings/settings_spritesheet.png', width, height)

    quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
    quit_button = Button((width / 2 - button_width * 3.5 / 2), (height / 2 + (button_height * 3.5 / 2) * 3),
                         quit_button,
                         3.5, screen, 'Assets/menu/quit/quit_spritesheet.png', width, height)

    title_name = TittleName(screen, width, height)

    menu_music.play(-1)
    run = True
    while run:

        screen.fill((0, 0, 0))
        inf += 2
        parallax(inf, scroll, folder)
        scroll += 4
        title_name.draw()
        start_button.draw()
        player_walk.update()
        player_walk.draw()
        princess_walk.update()
        princess_walk.draw()
        quit_button.draw()
        setting_button.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if start_button.clicked():
                run = False
                menu_music.soundtrack.stop()
                end('Assets/background/sunset_sky')

            if quit_button.clicked():
                run = False
                menu_music.soundtrack.stop()

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)
        pygame.display.update()
    pygame.quit()
