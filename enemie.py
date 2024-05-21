import pygame
from constants import (MAP_COLLISION_LAYER, GRAVITY, ENEMIES_SCALE, SCREEN_HEIGHT, ENEMIES_LIFE, ENEMIES_DAMAGE,
                       ENEMIES_ATTACK_DELAY)


class Enemies(object):
    def __init__(self, liste_pos, currentlevel, playergroup, bulletgroup, player):
        self.list_pos = liste_pos
        self.enemies_group = pygame.sprite.Group()
        self.current_level = currentlevel
        self.damage = ENEMIES_DAMAGE
        self.life = ENEMIES_LIFE
        Enemie.player = player
        Enemie.bullet_group = bulletgroup
        Enemie.player_group = playergroup
        for pos in self.list_pos:
            self.enemies_group.add(Enemie(self.damage, self.life, pos, self.current_level))

    def update(self):
        self.enemies_group.update()

    def draw(self, screen):
        self.enemies_group.draw(screen)

    def next_level(self, liste_pos, currentlevel, playergroup, bulletgroup, player):
        self.list_pos = liste_pos
        self.enemies_group = pygame.sprite.Group()
        self.current_level = currentlevel
        Enemie.player = player
        Enemie.bullet_group = bulletgroup
        Enemie.player_group = playergroup

        for pos in self.list_pos:
            self.enemies_group.add(Enemie(self.damage, self.life, pos, self.current_level))


class Enemie(pygame.sprite.Sprite):
    gravity = GRAVITY  # ajoute la gravité à la vitesse
    bullet_group = None  # Assigner les balles à cette variable depuis l'extérieur
    player = None  # permet d'avoir accès au joueur
    player_group = None  # Assigner le joueur à cette variable depuis l'extérieur

    def __init__(self, damage, life, pos, currentlevel):
        super().__init__()
        from spritesheet import SpriteSheet2
        self.sprites = SpriteSheet2("Assets/bullet/bullet.png")  # Charger l'image de l'ennemi
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
            self.animation[i] = pygame.transform.scale(image, (int(image_width * ENEMIES_SCALE),
                                                               int(image_height * ENEMIES_SCALE)))
        self.image = self.animation[0]
        self.life = life
        self.damage = damage  # Définir les dégâts de la balle
        self.attacktime = pygame.time.get_ticks()
        self.speed_x = 0  # Définir la vitesse en x
        self.speed_y = 0  # Définir la vitesse en y
        self.fall = True
        # Définit la position de l'ennemi
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.currentLevel.levelShift
        self.rect.y = pos[1] - self.currentLevel.levelShifty - self.rect.height
        self.shift = self.currentLevel.levelShift
        self.shifty = self.currentLevel.levelShifty

    def update(self):
        self.image = self.animation[self.frame]

        # Mise à jour de la position horizontale (equation de trajectoire)
        self.speed_y += Enemie.gravity  # Applique la gravité
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
        # if not self.fall and not tilehitlist: # inverse la direction pour éviter la chute (non fonctionnel)
        #     self.speed_x = -self.speed_x
        #     self.rect.x += self.speed_x * 2
        #     self.rect.y -= self.speed_y
        #     self.speed_y = 0
        self.shifty = self.currentLevel.levelShifty

        # Supprime l'ennemi si il sort de la map
        if (((self.rect.x - self.currentLevel.levelShift) > self.currentLevel.map_width) or
                ((self.rect.x - self.currentLevel.levelShift) < 0)):
            self.kill()
        if (self.rect.y + self.currentLevel.levelShifty) > self.currentLevel.map_height:
            self.kill()

        # Vérifie les collisions avec le joueur
        if Enemie.player_group is not None:
            hitlist = pygame.sprite.spritecollide(self, Enemie.player_group, False)

            if hitlist and (pygame.time.get_ticks() - self.attacktime) > ENEMIES_ATTACK_DELAY:  # delai d'attaque
                Enemie.player.life -= self.damage  # Inflige des dégâts au joueur
                self.attacktime = pygame.time.get_ticks()

        # Vérifie les collisions avec les balles qui sont tirées par le joueur
        if Enemie.bullet_group is not None:
            hitlist = pygame.sprite.spritecollide(self, Enemie.bullet_group, True)
            for bullet in hitlist:
                self.life -= bullet.damage   # Inflige des dégâts au joueur

        # Se tue si sa vie est épuisée
        if self.life <= 0:
            self.kill()

        # Animation de l'ennemi
        if pygame.time.get_ticks() - self.frametime > 100:
            self.frame = (self.frame + 1) % len(self.animation)
            self.frametime = pygame.time.get_ticks()

    def draw(self, screen):
        # affiche l'ennemi
        screen.blit(self.image, self.rect)
