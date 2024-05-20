import pygame
from constants import MAP_COLLISION_LAYER, GRAVITY, BULLET_SCALE

class Bullet(pygame.sprite.Sprite):
    gravity = GRAVITY
    player = None  # Assigner le joueur à cette variable depuis l'extérieur
    enemies = None  # Assigner les ennemis à cette variable depuis l'extérieur

    def __init__(self, damage, speed_x, speed_y, pos, currentlevel, byplayer):
        pygame.sprite.Sprite.__init__(self)
        from spritesheet import SpriteSheet2
        self.sprites = SpriteSheet2("Assets/bullet/bullet.png")  # Charger l'image de la balle
        self.animation = [self.sprites.image_at((0, 0, 6, 6)),
                          self.sprites.image_at((6, 0, 6, 6)),
                          self.sprites.image_at((12, 0, 6, 6))]
        self.image = self.animation[0]
        self.frame = 0
        image_width = self.image.get_width()
        image_height = self.image.get_height()
        for i, image in enumerate(self.animation):
            self.animation[i] = pygame.transform.scale(image, (int(image_width * BULLET_SCALE),
                                                               int(image_height * BULLET_SCALE)))

        # Set player position
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.damage = damage  # Définir les dégâts de la balle
        self.speed_x = speed_x  # Définir la vitesse en x
        self.speed_y = speed_y  # Définir la vitesse en y
        self.currentLevel = currentlevel
        self.byplayer = byplayer

    def update(self):  # TODO à appeler dans la boucle de jeu, player et enemies sont dans un groupe
        self.image = self.animation[self.frame]
        # Mettre à jour la position de la balle
        self.speed_y += Bullet.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # suprime la balle si elle sort de la map
        if (((self.rect.x - self.currentLevel.levelShift) > self.currentLevel.map_width) or
                (self.rect.x - self.currentLevel.levelShift) < 0):
            print("out x")
            self.kill()
        if (self.rect.y + self.currentLevel.levelShifty) > self.currentLevel.map_height:
            print("out y")
            self.kill()

        tilehitlist = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        if len(tilehitlist) > 0:
            self.kill()

        if self.byplayer:
            pass

        else:
            hitlist = pygame.sprite.spritecollide(self, Bullet.player, False)
            if hitlist:
                self.kill()

        if self.frame == 2:
            self.frame = 0
        else:
            self.frame += 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
