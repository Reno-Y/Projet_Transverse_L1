import pygame
import time
import os
from Class import spritesheet

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


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


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


def menu_back_apparition():
    background = pygame.image.load('Assets/menu/menu.png')
    background = pygame.transform.scale(background, (width, height))

    for i in range(0, 256, 10):  # fait apparaitre l'image
        screen.fill((0, 0, 0))
        background.set_alpha(i)
        screen.blit(background, (0, 0))
        pygame.display.update()


def menu_sound_and_apparition():
    menu_music = pygame.mixer.Sound("sound/music/theme_of_love.mp3")
    menu_music.play(-1)
    menu_back_apparition()


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


def main_menu(folder):
    scroll = 0
    inf = 0
    menu_sound_and_apparition()

    title_name = pygame.image.load('Assets/menu/Chronicles_of_Etheria.png').convert_alpha()
    title_name= pygame.transform.scale(title_name, (width, height))
    title_name.set_colorkey((255, 255, 255))

    princess_sheet = pygame.image.load('Assets/character/hime/walk.png').convert_alpha()
    princess = spritesheet(princess_sheet)

    princess_animation_list = []
    princess_animation_steps = 8
    last_update = pygame.time.get_ticks()
    animation_cooldown = 100
    frame = 0

    for i in range(princess_animation_steps):
        princess_animation_list.append(princess.get_image(i, 128, 128, 2, (0, 255, 246)))

    player_sheet = pygame.image.load('Assets/character/player/Run.png').convert_alpha()
    player_animation = spritesheet(player_sheet)

    player_animation_list = []
    player_animation_steps = 7

    for i in range(player_animation_steps):
        player_animation_list.append(player_animation.get_image(i, 128, 128, 2.5, (0, 255, 246)))



    run = True
    while run:

        screen.fill((0, 0, 0))
        inf += 2
        parallax(inf, scroll, folder)
        scroll += 5

        screen.blit(title_name, (0, 0))

        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            last_update = current_time
            frame += 1
            if frame >= len(princess_animation_list):
                frame = 0

        screen.blit(princess_animation_list[frame], (width - (width / 4), height - (height / 2.2)))

        if current_time - last_update >= animation_cooldown:
            last_update = current_time
            frame += 1
            if frame >= len(player_animation_list):
                frame = 0

        screen.blit(player_animation_list[frame - 1], ((width / 4) - 300, height - (height / 1.95)))

        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                run = False
            if event.type == pygame.QUIT:
                run = False
        clock.tick(60)
        pygame.display.update()
    pygame.quit()
