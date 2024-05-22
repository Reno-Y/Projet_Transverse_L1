import pygame
from constants import (MAP_COLLISION_LAYER, GRAVITY, ENEMIES_SCALE, ENEMIES_LIFE, ENEMIES_DAMAGE,
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
    gravity = GRAVITY  # Ajoute la gravité à la vitesse
    bullet_group = None  # Assigne les balles à cette variable depuis l'extérieur
    player = None  # Permet d'avoir accès au joueur
    player_group = None  # Assigne le joueur à cette variable depuis l'extérieur

    def __init__(self, damage, life, pos, currentlevel):
        super().__init__()
        from spritesheet import SpriteSheet2
        self.sprites = SpriteSheet2("Assets/cristal.png")  # Charge l'image de l'ennemi
        self.gemFull = [self.sprites.image_at((21, 0, 21, 25)),
                        self.sprites.image_at((42, 0, 21, 25)),
                        self.sprites.image_at((63, 0, 21, 25)),
                        self.sprites.image_at((84, 0, 21, 25)),
                        self.sprites.image_at((105, 0, 21, 25)),
                        self.sprites.image_at((126, 0, 21, 25)),
                        self.sprites.image_at((147, 0, 21, 25)),
                        self.sprites.image_at((168, 0, 21, 25)),
                        self.sprites.image_at((189, 0, 21, 25)),
                        self.sprites.image_at((210, 0, 21, 25)),
                        self.sprites.image_at((231, 0, 21, 25)),
                        self.sprites.image_at((252, 0, 21, 25)),
                        self.sprites.image_at((273, 0, 21, 25)),
                        self.sprites.image_at((294, 0, 21, 25))]

        self.gemHurt = [self.sprites.image_at((21, 32, 21, 25)),
                        self.sprites.image_at((42, 32, 21, 25)),
                        self.sprites.image_at((63, 32, 21, 25)),
                        self.sprites.image_at((84, 32, 21, 25)),
                        self.sprites.image_at((105, 32, 21, 25)),
                        self.sprites.image_at((126, 32, 21, 25)),
                        self.sprites.image_at((147, 32, 21, 25)),
                        self.sprites.image_at((168, 32, 21, 25)),
                        self.sprites.image_at((189, 32, 21, 25)),
                        self.sprites.image_at((210, 32, 21, 25)),
                        self.sprites.image_at((231, 32, 21, 25)),
                        self.sprites.image_at((252, 32, 21, 25)),
                        self.sprites.image_at((273, 32, 21, 25)),
                        self.sprites.image_at((294, 32, 21, 25))]

        self.gemDest = [self.sprites.image_at((21, 64, 21, 25)),
                        self.sprites.image_at((42, 64, 21, 25)),
                        self.sprites.image_at((63, 64, 21, 25)),
                        self.sprites.image_at((84, 64, 21, 25)),
                        self.sprites.image_at((105, 64, 21, 25)),
                        self.sprites.image_at((126, 64, 21, 25)),
                        self.sprites.image_at((147, 64, 21, 25)),
                        self.sprites.image_at((168, 64, 21, 25)),
                        self.sprites.image_at((189, 64, 21, 25)),
                        self.sprites.image_at((210, 64, 21, 25)),
                        self.sprites.image_at((231, 64, 21, 25)),
                        self.sprites.image_at((252, 64, 21, 25)),
                        self.sprites.image_at((273, 64, 21, 25)),
                        self.sprites.image_at((294, 64, 21, 25))]

        self.image = self.gemFull[0]
        image_width = self.image.get_width()
        image_height = self.image.get_height()

        for i, image in enumerate(self.gemFull):
            self.gemFull[i] = pygame.transform.scale(image, (int(image_width * ENEMIES_SCALE),
                                                             int(image_height * ENEMIES_SCALE)))
        for i, image in enumerate(self.gemHurt):
            self.gemHurt[i] = pygame.transform.scale(image, (int(image_width * ENEMIES_SCALE),
                                                             int(image_height * ENEMIES_SCALE)))
        for i, image in enumerate(self.gemDest):
            self.gemDest[i] = pygame.transform.scale(image, (int(image_width * ENEMIES_SCALE),
                                                             int(image_height * ENEMIES_SCALE)))

        self.currentLevel = currentlevel
        self.frame = 0
        self.frametime = pygame.time.get_ticks()
        self.life = life
        self.damage = damage  # Définit les dégâts de la balle
        self.attacktime = pygame.time.get_ticks()
        self.speed_x = 0  # Définit la vitesse en x
        self.speed_y = 0  # Définit la vitesse en y
        self.fall = True
        # Définit la position de l'ennemi et sa collision
        self.image = self.gemFull[0]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - self.currentLevel.levelShift
        self.rect.y = pos[1] - self.currentLevel.levelShifty - self.rect.height
        self.shift = self.currentLevel.levelShift
        self.shifty = self.currentLevel.levelShifty

    def update(self):

        if self.life >= 3:
            self.image = self.gemFull[self.frame]
        elif self.life == 2:
            self.image = self.gemHurt[self.frame]
        else:
            self.image = self.gemDest[self.frame]

        # Mise à jour de la position horizontale (équation de trajectoire)
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
        # if not self.fall and not tilehitlist: # Inverse la direction pour éviter la chute (non fonctionnel)
        #     self.speed_x = -self.speed_x
        #     self.rect.x += self.speed_x * 2
        #     self.rect.y -= self.speed_y
        #     self.speed_y = 0
        self.shifty = self.currentLevel.levelShifty

        # Supprime l'ennemi s'il sort de la carte
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
                self.life -= bullet.damage  # Inflige des dégâts au joueur

        # Se tue si sa vie est épuisée
        if self.life <= 0:
            self.kill()

        # Animation de l'ennemi
        if pygame.time.get_ticks() - self.frametime > 100:
            self.frame = (self.frame + 1) % len(self.gemFull)
            self.frametime = pygame.time.get_ticks()

    def draw(self, screen):
        # Affiche l'ennemi
        screen.blit(self.image, self.rect)
