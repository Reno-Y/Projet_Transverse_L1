import pygame

from bullet import Bullet
from constants import (GRAVITY, MAP_COLLISION_LAYER, SCREEN_HEIGHT, SCREEN_WIDTH, BULLET_SPEED, PLAYER_AIR_MOVE,
                       PLAYER_SPEED, PLAYER_DAMAGE, PLAYER_LIFE, PLAYER_DASH, PLAYER_SHOOT_DELAY, PLAYER_DASH_DELAY,
                       PLAYER_JUMP_ACCELERATION)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_pos):
        from spritesheet import SpriteSheet2
        pygame.sprite.Sprite.__init__(self)

        # Charge le sprite sheet du personnage/joueur
        self.sprites = SpriteSheet2("Assets/character/player/Player1.png")

        self.stillRight = self.sprites.image_at((0, 0, 48, 60))
        self.stillLeft = self.sprites.image_at((0, 64, 48, 64))

        # Liste des frames pour chaque animation
        self.runningRight = (self.sprites.image_at((48, 0, 50, 64)),
                             self.sprites.image_at((102, 0, 50, 64)),
                             self.sprites.image_at((150, 0, 50, 64)),
                             self.sprites.image_at((251, 0, 50, 64)),
                             self.sprites.image_at((300, 0, 50, 64)),
                             self.sprites.image_at((354, 0, 50, 64)),
                             self.sprites.image_at((402, 0, 50, 64)))

        self.runningLeft = (self.sprites.image_at((48, 64, 50, 63)),
                            self.sprites.image_at((102, 64, 50, 63)),
                            self.sprites.image_at((150, 64, 50, 63)),
                            self.sprites.image_at((251, 64, 50, 63)),
                            self.sprites.image_at((300, 64, 50, 63)),
                            self.sprites.image_at((354, 64, 50, 63)),
                            self.sprites.image_at((402, 64, 50, 63)))

        self.jumpingLeft = \
            (self.sprites.image_at((61, 128, 50, 64)),
             self.sprites.image_at((107, 128, 50, 64)),
             self.sprites.image_at((156, 128, 50, 64)))

        self.jumpingRight = (self.sprites.image_at((49, 192, 48, 64)),
                             self.sprites.image_at((95, 192, 50, 64)),
                             self.sprites.image_at((156, 192, 50, 64)))

        self.image = self.stillRight

        # Fixe la position du joueur
        self.rect = self.image.get_rect()
        self.rect.x = player_pos[0]
        self.rect.y = player_pos[1]

        # Fix la vitesse et la direction du joueur
        self.speedX = 0
        self.speedY = 0
        self.direction = "right"

        # Booléen pour savoir si le joueur court
        # 1ère frame dans l'animation de course du joueur
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # Niveau actuel du joueur
        self.currentLevel = None
        self.difference = 0
        self.difference_y = 0
        self.dash_time = pygame.time.get_ticks()
        self.shoot_time = pygame.time.get_ticks()
        self.dashing = 0  # Nombre d'images avant la fin du dash
        self.damage = PLAYER_DAMAGE
        self.life = PLAYER_LIFE

    def update(self):
        if self.dashing > 0:
            if self.direction == "right":
                self.speedX = 10
            else:
                self.speedX = -10
            self.dashing -= 1

        # Change la caméra si le joueur atteint le bord droit de l'écran (pour que la caméra suive le joueur)
        if ((self.rect.right >= SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) and
                ((SCREEN_WIDTH - self.currentLevel.levelShift) < self.currentLevel.map_width)):

            self.difference = -(self.rect.right - (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)))
            self.rect.right = SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)

        # Change la caméra si le joueur atteint le bord gauche de l'écran
        elif (self.rect.left <= (SCREEN_WIDTH * 0.3)) and 0 > self.currentLevel.levelShift:

            self.difference = (SCREEN_WIDTH * 0.3) - self.rect.left
            self.rect.left = (SCREEN_WIDTH * 0.3)

        # Change la caméra si le joueur atteint le bord inférieur de l'écran
        if ((self.rect.bottom >= SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)) and
                ((self.currentLevel.map_height - self.currentLevel.levelShifty) < SCREEN_HEIGHT)):

            self.difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)))
            self.rect.bottom = SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)

        # Change la camera si le joueur atteint le bord supérieur de l'écran
        elif self.rect.top <= (SCREEN_HEIGHT * 0.15):
            self.difference_y = (SCREEN_HEIGHT * 0.15) - self.rect.top
            self.rect.top = (SCREEN_HEIGHT * 0.15)
        self.currentLevel.shiftLevel(self.difference, self.difference_y)
        self.difference_y, self.difference = 0, 0

    # collision du joueur

        # Met à jour la position x du joueur
        self.rect.x += self.speedX
        # Récupère les tuiles de la couche de collision que le joueur est en train de toucher
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # Déplace le joueur du bon côté de ce bloc
        for tile in tileHitList:
            if self.speedX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
        self.speedX = 0


        # Met à jour la position y du joueur
        self.rect.y += self.speedY

        # Récupère les tuiles de la couche de collision que le joueur est en train de toucher
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # S'il y a des tuiles dans cette liste
        if len(tileHitList) > 0:
            # Déplace le joueur sur le bon côté de la tuile, puis met à jour le cadre du joueur
            for tile in tileHitList:
                if self.speedY > 0:
                    self.rect.bottom = tile.rect.top
                    self.speedY = 1

                    if self.direction == "right":
                        self.image = self.stillRight
                    else:
                        self.image = self.stillLeft
                else:
                    self.rect.top = tile.rect.bottom
                    self.speedY = 0
        # S'il n'y a pas des tuiles dans cette liste
        else:
            # Update player change for jumping/falling and player frame
            self.speedY += GRAVITY
            if self.speedY > 0:
                if self.direction == "right":
                    self.image = self.jumpingRight[1]
                else:
                    self.image = self.jumpingLeft[1]

        # If player is on ground and running, update running animation
        if self.running and self.speedY == 1:
            if self.direction == "right":
                self.image = self.runningRight[self.runningFrame]
            else:
                self.image = self.runningLeft[self.runningFrame]

        # When correct amount of time has passed, go to next frame
        if pygame.time.get_ticks() - self.runningTime > 100:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

    def jump(self):
        # Check if player is on ground
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tileHitList) > 0:
            if self.direction == "right":
                self.image = self.jumpingRight[0]
            else:
                self.image = self.jumpingLeft[0]

            self.speedY += PLAYER_JUMP_ACCELERATION

    def dash(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tileHitList) > 0 and PLAYER_DASH:
            if (pygame.time.get_ticks() - self.dash_time) > PLAYER_DASH_DELAY:
                self.dashing = 10
                self.dash_time = pygame.time.get_ticks()

    #  Move right
    def goRight(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if (len(tileHitList) > 0) or PLAYER_AIR_MOVE:
            self.direction = "right"
            self.running = True
            self.speedX = PLAYER_SPEED

    # Move left
    def goLeft(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if (len(tileHitList) > 0) or PLAYER_AIR_MOVE:
            self.direction = "left"
            self.running = True
            self.speedX = -PLAYER_SPEED

    # Stop moving
    def stop(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tileHitList) > 0 and (self.dashing <= 0):
            self.running = False
            self.speedX = 0

    def shoot(self, display, mouse_pos):
        if (pygame.time.get_ticks() - self.shoot_time) > PLAYER_SHOOT_DELAY:
            # Calcule les composantes du vecteur direction
            direction_x = ((mouse_pos[0] - self.rect.x) * BULLET_SPEED) / SCREEN_WIDTH
            direction_y = ((mouse_pos[1] - self.rect.y) * BULLET_SPEED) / SCREEN_HEIGHT

            # Multipliées par la vitesse souhaitée
            speed_x = min(direction_x, BULLET_SPEED)
            speed_y = min(direction_y, BULLET_SPEED)
            self.shoot_time = pygame.time.get_ticks()
            # Créé et retourne la nouvelle balle
            return Bullet(self.damage, speed_x, speed_y, self.rect.center, self.currentLevel, True)

    # Draw player
    def draw(self, screen):
        screen.blit(self.image, self.rect)
