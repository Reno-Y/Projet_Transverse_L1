import pygame
MAP_COLLISION_LAYER = 1


class Bullet(pygame.sprite.Sprite):
    gravity = 1

    def __init__(self, damage, speed_x, speed_y, pos, currentlevel,  display, byplayer):
        super().__init__()
        from spritesheet import SpriteSheet2
        self.sprites = SpriteSheet2("Assets/bullet/bullet.png")  # Charger l'image de la balle
        self.animation = (self.sprites.image_at((0, 0, 6, 6)),
                          self.sprites.image_at((6, 0, 6, 6)),
                          self.sprites.image_at((12, 0, 6, 6)))
        self.image = self.animation[0]
        self.rect = self.image.get_rect()  # Obtenir le rectangle de l'image
        self.rect.topleft = pos  # Positionner la balle à la position donnée

        self.damage = damage  # Définir les dégâts de la balle
        self.speed_x = speed_x  # Définir la vitesse en x
        self.speed_y = speed_y  # Définir la vitesse en y
        self.currentLevel = currentlevel
        self.display = display
        self.byplayer = byplayer


    def update(self, enemies, player): #TODO à appeler dans la boucle de jeu player et enemies sont dans un groupe
        self.display.blit(self.image, self.rect)
        # Mettre à jour la position de la balle
        self.speed_y += Bullet.gravity
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        tilehitlist = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        if len(tilehitlist) > 0:
            self.kill()
            return []
        if self.byplayer:
            hitlist = pygame.sprite.spritecollide(self, enemies, False)
            self.kill()
            return hitlist
        else:
            hitlist = pygame.sprite.spritecollide(self, player, False)
            self.kill()
            return hitlist


def shoot(self, display, mouse_pos): #TODO dans player faut completer les attributs
    # Calculer le vecteur de direction
    direction_x = mouse_pos[0] - self.rect.x
    direction_y = mouse_pos[1] - self.rect.y

    # Multiplier par la vitesse souhaitée
    speed_x = max(direction_x, 100)
    speed_y = max(direction_y, 100)

    # Créer et retourner la nouvelle balle
    return Bullet(self.damage, speed_x, speed_y, self.rect.topleft, self.currentLevel, display, True)
    #TODO à ajouter a un groupe dans la boucle de jeu

