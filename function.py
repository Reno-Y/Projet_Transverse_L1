import pygame
import time
import os

pygame.init()
pygame.mixer.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))
pygame.font.init()
title_font = pygame.font.Font("Assets/font/hero-speak.ttf", 60)
canvas = pygame.Surface((width, height))
clock = pygame.time.Clock()


def game_window_info():
    pygame.display.set_caption('Chronicles of Etheria')
    game_icon = pygame.image.load('Assets/menu/Shinobi_studio.png')
    pygame.display.set_icon(game_icon)
    # on définit le titre et l'icône de la fenêtre


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


def parallax_init(folder):
    bg_images = background_images_list(folder)
    return bg_images


def parallax(scroll, bg_images, d_screen):
    speed = 1
    for y in bg_images:
        i = (scroll * speed) // width
        x_position = -scroll * speed
        while x_position < width:
            d_screen.blit(y, ((i * width) - scroll * speed, 0))
            i += 1
            x_position += width
        speed += 1
    # on fait défiler les images de fond


def compute_penetration(block, old_rect, new_rect):
    dx_correction = dy_correction = 0.0
    if old_rect.bottom <= block.top < new_rect.bottom:
        dy_correction = block.top - new_rect.bottom
    elif old_rect.top >= block.bottom > new_rect.top:
        dy_correction = block.bottom - new_rect.top
    if old_rect.right <= block.left < new_rect.right:
        dx_correction = block.left - new_rect.right
    elif old_rect.left >= block.right > new_rect.left:
        dx_correction = block.right - new_rect.left
    return dx_correction, dy_correction
