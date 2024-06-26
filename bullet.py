import pygame
from constants import MAP_COLLISION_LAYER, GRAVITY, BULLET_SCALE


class Bullet(pygame.sprite.Sprite):
    gravity = GRAVITY
    player_group = None  # Assigne le joueur à cette variable depuis l'extérieur
    enemies_group = None  # Assigne les ennemis à cette variable depuis l'extérieur

    def __init__(self, damage, speed_x, speed_y, pos, currentlevel, byplayer):
        pygame.sprite.Sprite.__init__(self)
        from spritesheet import SpriteSheet2
        self.sprites = SpriteSheet2("Assets/bullet/bullet.png")  # Charge l'image de la balle
        self.animation = [self.sprites.image_at((0, 0, 6, 6)),
                          self.sprites.image_at((6, 0, 6, 6)),
                          self.sprites.image_at((12, 0, 6, 6))]
        self.image = self.animation[0]
        self.frame = 0
        self.frame_time = pygame.time.get_ticks()
        image_width = self.image.get_width()
        image_height = self.image.get_height()
        for i, image in enumerate(self.animation):
            self.animation[i] = pygame.transform.scale(image, (int(image_width * BULLET_SCALE),
                                                               int(image_height * BULLET_SCALE)))

        # Définit la position du joueur
        self.currentLevel = currentlevel
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

        self.damage = damage  # Définit les dégâts de la balle
        self.speed_x = speed_x  # Définit la vitesse en x
        self.speed_y = speed_y  # Définit la vitesse en y

        self.by_player = byplayer

    def update(self):
        self.image = self.animation[self.frame]

        # Met à jour la position de la balle (équation de trajectoire)
        self.speed_y += Bullet.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Supprime la balle si elle sort de la carte
        if (((self.rect.x - self.currentLevel.levelShift) > self.currentLevel.map_width) or
                (self.rect.x - self.currentLevel.levelShift) < 0):
            self.kill()
        if (self.rect.y + self.currentLevel.levelShifty) > self.currentLevel.map_height:
            self.kill()

        #  Supprime la balle si elle entre en collision avec la carte
        tilehitlist = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        if len(tilehitlist) > 0:
            self.kill()

        # Fait des dégats à l'ennemi et supprime la balle si elle entre en collision avec la carte
        if self.by_player and Bullet.enemies_group is not None:
            hitlist = pygame.sprite.spritecollide(self, Bullet.enemies_group, False)
            for enemie in hitlist:
                self.kill()
                enemie.life -= 1

        else:
            # Fait des dégâts au joueur et supprime la balle si elle entre en collision avec la carte
            if Bullet.player_group is not None and not self.by_player:
                hitlist = pygame.sprite.spritecollide(self, Bullet.player_group, False)
                for player in hitlist:
                    self.kill()
                    player.life -= 1

        if pygame.time.get_ticks() - self.frame_time > 100:
            if self.frame == 2:
                self.frame = 0
            else:
                self.frame += 1
            self.frame_time = pygame.time.get_ticks()

    def draw(self, screen):
        # Affiche la balle
        screen.blit(self.image, self.rect)
