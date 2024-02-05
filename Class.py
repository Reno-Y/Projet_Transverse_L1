import pygame

pygame.init()
width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((width, height))

class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, image_width, image_height, scale, color):
        image = pygame.Surface((image_width, image_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * image_width, 0, image_width, image_height))
        image = pygame.transform.scale(image, (image_width * scale, image_height * scale))
        image.set_colorkey(color)
        return image


class Animation:
    def __init__(self, screen, width, height, sheet_location, scale, sprite_pixel, coordinates):
        self.screen = screen
        self.width = width
        self.height = height
        self.sheet_location = sheet_location
        self.coordinates = coordinates
        sprite_sheet = pygame.image.load(sheet_location).convert_alpha()
        sheet_length = sprite_sheet.get_width()
        animation_step = sheet_length // sprite_pixel
        self.sprite = Spritesheet(sprite_sheet)
        self.sprite_animation_list = []
        self.sprite_animation_steps = animation_step
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0

        for i in range(animation_step):
            self.sprite_animation_list.append(
                self.sprite.get_image(i, sprite_pixel, sprite_pixel, scale, (0, 255, 246)))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.frame = (self.frame + 1) % len(self.sprite_animation_list)

    def draw(self):
        self.screen.blit(self.sprite_animation_list[self.frame], self.coordinates)

class Button:
    def __init__(self,x ,y ,image, scale):
        self.x = x
        self.y = y
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            pygame.draw.rect(screen, (255, 0, 0), self.rect)
        screen.blit(self.image, (self.rect.x, self.rect.y))