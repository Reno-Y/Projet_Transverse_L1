import pygame


def load_image(file_name):
    return pygame.image.load(file_name)


def get_frame(sheet, rectangle):
    rect = pygame.Rect(rectangle)
    image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
    image.blit(sheet, (0, 0), rect)
    return image

