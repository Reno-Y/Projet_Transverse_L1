import pygame
from constants import MAP_COLLISION_LAYER, GRAVITY, ENEMIE_SCALE, SCREEN_HEIGHT


class Enemies(object):
    def __init__(self, liste_pos, currentlevel, playergroup, bulletgroup, player):
        self.liste_pos = liste_pos
        self.enemies_group = pygame.sprite.Group()
        self.currentlevel = currentlevel
        self.domage = 2
        self.life = 3
        Enemie.player = player
        Enemie.bullet_group = bulletgroup
        Enemie.player_group = playergroup
        for pos in self.liste_pos:
            self.enemies_group.add(Enemie(self.domage, self.life, pos, self.currentlevel))

    def update(self):
        self.enemies_group.update()

    def draw(self, screen):
        self.enemies_group.draw(screen)


class Enemie(pygame.sprite.Sprite):
    gravity = GRAVITY  # Assurez-vous que GRAVITY est défini quelque part dans votre code
    bullet_group = None  # Assigner les balles à cette variable depuis l'extérieur
    player = None
    player_group = None  # Assigner le joueur à cette variable depuis l'extérieur

    def __init__(self, damage, life, pos, currentlevel):
        super().__init__()
        from spritesheet import SpriteSheet2
        self.sprites = SpriteSheet2("Assets/bullet/bullet.png")  # Charger l'image de l'enemie
        self.animation = [self.sprites.image_at((0, 0, 6, 6)),
                          self.sprites.image_at((6, 0, 6, 6)),
                          self.sprites.image_at((12, 0, 6, 6))]
        self.image = self.animation[0]
        self.currentLevel = currentlevel
        self.frame = 0
        self.frametime = pygame.time.get_ticks()
        image_width = self.image.get_width()
        image_height = self.image.get_height()
        for i, image in enumerate(self.animation):
            self.animation[i] = pygame.transform.scale(image, (int(image_width * ENEMIE_SCALE),
                                                               int(image_height * ENEMIE_SCALE)))
        self.image = self.animation[0]
        self.life = life
        self.damage = damage  # Définir les dégâts de la balle
        self.attacktime = pygame.time.get_ticks()
        self.speed_x = 2  # Définir la vitesse en x
        self.speed_y = 0  # Définir la vitesse en y
        self.fall = True
        # Set enemie position
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.currentLevel.levelShift
        self.rect.y = pos[1] - self.currentLevel.levelShifty
        self.shift = self.currentLevel.levelShift
        self.shifty = self.currentLevel.levelShifty

    def update(self):
        self.image = self.animation[self.frame]
        self.speed_y += Enemie.gravity  # Applique la gravité


        # Mise à jour de la position horizontale
        self.rect.x += self.speed_x + (self.currentLevel.levelShift - self.shift)
        self.shift = self.currentLevel.levelShift

        # Vérification des collisions horizontales
        tilehitlist = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        for tile in tilehitlist:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
            elif self.speed_x < 0:
                self.rect.left = tile.rect.right
            self.speed_x = -self.speed_x  # Inverse la direction de déplacement

        # Mise à jour de la position verticale
        self.rect.y += self.speed_y + (self.currentLevel.levelShifty - self.shifty)
        tilehitlist = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        if tilehitlist:
            for tile in tilehitlist:
                if self.speed_y >= 0:
                    self.rect.bottom = tile.rect.top
                elif self.speed_y > 0:
                    self.rect.top = tile.rect.bottom
                self.speed_y = 0  # Arrête la chute en cas de collision
                self.fall = False
        if not self.fall and not tilehitlist:
            self.speed_x = -self.speed_x
            self.rect.x += self.speed_x * 2
            self.rect.y -= self.speed_y
            self.speed_y = 0

        self.shifty = self.currentLevel.levelShifty


        # Supprime l'enemie si elle sort de la map
        if self.rect.x > self.currentLevel.map_width or self.rect.x < 0:
            self.kill()
        if self.rect.y > self.currentLevel.map_height + SCREEN_HEIGHT:
            self.kill()

        # Vérifie les collisions avec le joueur
        if Enemie.player_group is not None:
            hitlist = pygame.sprite.spritecollide(self, Enemie.player_group, False)
            if hitlist and (pygame.time.get_ticks() - self.attacktime) > 1000:  # delai d'attaque
                Enemie.player.life -= self.damage  # Inflige des dégâts au joueur
                self.attacktime = pygame.time.get_ticks()

        if Enemie.bullet_group is not None:
            hitlist = pygame.sprite.spritecollide(self, Enemie.bullet_group, True)
            for bullet in hitlist:
                self.life -= bullet.damage   # Inflige des dégâts au joueur

        # Tue l'enemie si sa vie est épuisée
        if self.life <= 0:
            self.kill()

        # Animation de l'enemie
        if pygame.time.get_ticks() - self.frametime > 100:
            self.frame = (self.frame + 1) % len(self.animation)
            self.frametime = pygame.time.get_ticks()

    def draw(self, screen):

        screen.blit(self.image, self.rect)
