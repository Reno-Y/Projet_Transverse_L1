import pygame

pygame.init()


class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, image_width, image_height, scale, color):
        image = pygame.Surface((image_width, image_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * image_width, 0, image_width, image_height))
        image = pygame.transform.scale(image, (image_width * scale, image_height * scale))
        image.set_colorkey(color)
        return image


class TittleName:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        title_image = pygame.image.load('Assets/menu/Chronicles_of_Etheria.png').convert_alpha()
        self.title_image = pygame.transform.scale(title_image, (self.width, self.height))

    def draw(self):
        self.screen.blit(self.title_image, (0, 0))


class Music:
    def __init__(self, music_location):
        self.soundtrack = pygame.mixer.Sound(music_location)

    def play(self, loop):
        self.soundtrack.play(loop)


class Animation:
    def __init__(self, screen, width, height, sheet_location, scale, pixel_x, pixel_y, coordinates):
        self.screen = screen
        self.width = width
        self.height = height
        self.sheet_location = sheet_location
        self.coordinates = coordinates
        sprite_sheet = pygame.image.load(sheet_location).convert_alpha()
        sheet_length = sprite_sheet.get_width()
        animation_step = sheet_length // pixel_x
        self.sprite = Spritesheet(sprite_sheet)
        self.sprite_animation_list = []
        self.sprite_animation_steps = animation_step
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0

        for i in range(animation_step):
            self.sprite_animation_list.append(
                self.sprite.get_image(i, pixel_x, pixel_y, scale, (0, 255, 246)))

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.frame = (self.frame + 1) % len(self.sprite_animation_list)

    def draw(self):
        self.screen.blit(self.sprite_animation_list[self.frame], self.coordinates)


class Button:
    def __init__(self, x, y, image, scale, screen, sheet, width, height):
        self.x = x
        self.y = y
        image_width = image.get_width()
        image_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        self.scale = scale
        self.screen = screen
        self.sheet = sheet
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height
        self.button_animation = Animation(screen, width, height, sheet, scale, 64, 16,
                                          (x, y))

    def clicked(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            return True

    def draw(self):
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            self.button_animation.update()
            self.button_animation.draw()
        elif not self.rect.collidepoint(pos):
            self.screen.blit(self.image, (self.rect.x, self.rect.y))

