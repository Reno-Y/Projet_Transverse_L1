import pygame
pygame.init()


class Button:
    def __init__(self, x, y, image, scale, screen, sheet, width, height):
        from animation import Animation
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
            # Vérifie si le bouton est cliqué

            return True

    def draw(self):
        pos = pygame.mouse.get_pos()  # Récupère la position de la souris

        if self.rect.collidepoint(pos):
            self.button_animation.update()
            self.button_animation.draw()
            # Affiche l'animation du bouton si la souris est dessus

        elif not self.rect.collidepoint(pos):
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
            # Affiche l'image du bouton si la souris n'est pas dessus
