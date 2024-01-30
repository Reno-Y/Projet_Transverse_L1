import pygame

pygame.init()


class spritesheet:

    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, image_width, image_height, scale,color):
        image = pygame.Surface((image_width, image_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * image_width, 0, image_width, image_height))
        image = pygame.transform.scale(image, (image_width * scale, image_height * scale))
        image.set_colorkey(color)
        return image
