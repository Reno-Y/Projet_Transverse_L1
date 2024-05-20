import pygame


class Animation:
    def __init__(self, screen, width, height, sheet_location, scale, pixel_x, pixel_y, coordinates):
        from spritesheet import Spritesheet

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
        self.animation_cooldown = 150
        self.frame = 0
        self.finished = False

        for i in range(animation_step):
            self.sprite_animation_list.append(
                self.sprite.get_image(i, pixel_x, pixel_y, scale, (0, 255, 246)))
            # On récupère les images de l'animation par leurs formats
            # On génère une liste d'images pour l'animation

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.frame = (self.frame + 1) % len(self.sprite_animation_list)
            # on change de frame à chaque fois que le cooldown est atteint

    def draw(self, orientation=None):
        self.screen.blit(self.sprite_animation_list[self.frame], self.coordinates)

        if orientation is not None:  # on inverse l'image
            self.screen.blit(pygame.transform.flip(self.sprite_animation_list[self.frame], False, True),
                             self.coordinates)
        # on affiche la frame actuelle

    def play_once(self,animation_cooldown):
        """Joue l'animation une seule fois"""
        current_time = pygame.time.get_ticks()
        if not self.finished and current_time - self.last_update >= animation_cooldown:
            self.last_update = current_time
            self.frame += 1
            if self.frame >= len(self.sprite_animation_list):
                self.frame = len(self.sprite_animation_list) - 1
                self.finished = True  # Marque l'animation comme terminée

    def is_finished(self):
        """Retourne True si l'animation est terminée"""
        return self.finished