import pygame

from bullet import Bullet
from constants import (GRAVITY, MAP_COLLISION_LAYER, SCREEN_HEIGHT, SCREEN_WIDTH, BULLET_SPEED, PLAYER_AIR_MOVE,
                       PLAYER_SPEED, PLAYER_DAMAGE, PLAYER_LIFE, PLAYER_DASH, PLAYER_SHOOT_DELAY, PLAYER_DASH_DELAY,
                       PLAYER_JUMP_ACCELERATION)


class Player(pygame.sprite.Sprite):
    def __init__(self, player_pos):
        from spritesheet import SpriteSheet2
        pygame.sprite.Sprite.__init__(self)

        # Load the sprite-sheet for this player
        self.sprites = SpriteSheet2("Assets/character/player/Player.png")

        # Load the frames for each animation

        self.stillRight = self.sprites.image_at((0, 256, 43, 64))

        self.stillLeft = self.sprites.image_at((0, 320, 43, 64))

        # List of frames for each animation
        self.runningRight = (self.sprites.image_at((64, 0, 54, 64)),
                             self.sprites.image_at((128, 0, 54, 64)),
                             self.sprites.image_at((192, 0, 54, 64)),
                             self.sprites.image_at((256, 0, 54, 64)),
                             self.sprites.image_at((320, 0, 54, 64)),
                             self.sprites.image_at((384, 0, 54, 64)),
                             self.sprites.image_at((448, 0, 54, 64)))

        self.runningLeft = (self.sprites.image_at((64, 64, 54, 64)),
                            self.sprites.image_at((128, 64, 54, 64)),
                            self.sprites.image_at((192, 64, 54, 64)),
                            self.sprites.image_at((256, 64, 54, 64)),
                            self.sprites.image_at((320, 64, 54, 64)),
                            self.sprites.image_at((384, 64, 54, 64)),
                            self.sprites.image_at((448, 64, 54, 64)))

        self.jumpingRight = \
            (self.sprites.image_at((64, 128, 50, 64)),
             self.sprites.image_at((128, 128, 50, 64)),
             self.sprites.image_at((192, 128, 50, 64)))

        self.jumpingLeft = (self.sprites.image_at((64, 192, 50, 64)),
                            self.sprites.image_at((128, 192, 50, 64)),
                            self.sprites.image_at((192, 192, 50, 64)))

        self.image = self.stillRight

        # Définit la position du joueur
        self.rect = self.image.get_rect()
        self.rect.x = player_pos[0]
        self.rect.y = player_pos[1]

        # Définit la vitesse et la direction du joueur
        self.speedX = 0
        self.speedY = 0
        self.direction = "right"

        # Booléen pour vérifier si le joueur court, la frame actuelle de l'animation de course et
        # le temps depuis le dernier changement de frame
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # Niveau actuel où se trouve le joueur, défini après l'initialisation de l'objet dans le jeu
        self.currentLevel = None
        self.difference = 0
        self.difference_y = 0
        self.dash_time = pygame.time.get_ticks()
        self.shoot_time = pygame.time.get_ticks()
        self.dashing = 0  # nombre d'images avant la fin du dash
        self.damage = PLAYER_DAMAGE
        self.life = PLAYER_LIFE

    def update(self):
        if self.dashing > 0:
            if self.direction == "right":
                self.speedX = 3 * PLAYER_SPEED
            else:
                self.speedX = -3 * PLAYER_SPEED
            self.dashing -= 1

        # Change la camera si le joueur atteint le bord droit de l'écran
        if ((self.rect.right >= SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) and
                ((SCREEN_WIDTH - self.currentLevel.levelShift) < self.currentLevel.map_width)):

            self.difference = -(self.rect.right - (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)))
            self.rect.right = SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)

        # Change la camera si le joueur atteint le bord gauche de l'écran
        elif (self.rect.left <= (SCREEN_WIDTH * 0.3)) and 0 > self.currentLevel.levelShift:

            self.difference = (SCREEN_WIDTH * 0.3) - self.rect.left
            self.rect.left = (SCREEN_WIDTH * 0.3)

        # Change la camera si le joueur atteint le bord inférieur de l'écran
        if ((self.rect.bottom >= SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)) and
                ((self.currentLevel.map_height - self.currentLevel.levelShifty) < SCREEN_HEIGHT)):

            self.difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)))
            self.rect.bottom = SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)

        # Change la camera si le joueur atteint le bord supérieur de l'écran
        elif self.rect.top <= (SCREEN_HEIGHT * 0.15):
            self.difference_y = (SCREEN_HEIGHT * 0.15) - self.rect.top
            self.rect.top = (SCREEN_HEIGHT * 0.15)
        self.currentLevel.shift_level(self.difference, self.difference_y)
        self.difference_y, self.difference = 0, 0

    # Collision du joueur

        # Met à jour la position x du joueur
        self.rect.x += self.speedX
        # Récupère les tuiles de la couche de collision que le joueur est en train de toucher
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # Déplace le joueur du bon côté du block
        for tile in tile_hit_list:
            if self.speedX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
        self.speedX = 0


        # Met à jour la position y du joueur
        self.rect.y += self.speedY

        # Récupère les tuiles de la couche de collision que le joueur est en train de toucher
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # S'il y a des tuiles dans cette liste
        if len(tile_hit_list) > 0:
            # Dépalce le joueur du bon côté de la tuile, ainsi que sa frame
            for tile in tile_hit_list:
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
        # S'il n'y a pas de tuiles dans la liste
        else:
            # Met à jour les sauts et chutes du joueur, ainsi que ses frames
            self.speedY += GRAVITY
            if self.speedY > 0:
                if self.direction == "right":
                    self.image = self.jumpingRight[1]
                else:
                    self.image = self.jumpingLeft[1]

        # Si le joueur court sur le sol, met à jour son animation de course
        if self.running and self.speedY == 1:
            if self.direction == "right":
                self.image = self.runningRight[self.runningFrame]
            else:
                self.image = self.runningLeft[self.runningFrame]

        # Quand la durée est écoulée, passe à la prochaine frame
        if pygame.time.get_ticks() - self.runningTime > 100:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

    def jump(self):
        # Vérifie si le joueur est sur le sol
        self.rect.y += 2
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tile_hit_list) > 0:
            if self.direction == "right":
                self.image = self.jumpingRight[0]
            else:
                self.image = self.jumpingLeft[0]

            self.speedY += PLAYER_JUMP_ACCELERATION

    def dash(self):
        self.rect.y += 2
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tile_hit_list) > 0 and PLAYER_DASH:
            if (pygame.time.get_ticks() - self.dash_time) > PLAYER_DASH_DELAY:
                self.dashing = 10
                self.dash_time = pygame.time.get_ticks()

    #  Move right
    def go_right(self):
        self.rect.y += 2
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if (len(tile_hit_list) > 0) or PLAYER_AIR_MOVE:
            self.direction = "right"
            self.running = True
            self.speedX = PLAYER_SPEED

    # Move left
    def go_left(self):
        self.rect.y += 2
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if (len(tile_hit_list) > 0) or PLAYER_AIR_MOVE:
            self.direction = "left"
            self.running = True
            self.speedX = -PLAYER_SPEED

    # Empêche le joueur d'avancer
    def stop(self):
        self.rect.y += 2
        tile_hit_list = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tile_hit_list) > 0 and (self.dashing <= 0):
            self.running = False
            self.speedX = 0

    def shoot(self, mouse_pos):
        if (pygame.time.get_ticks() - self.shoot_time) > PLAYER_SHOOT_DELAY:
            # Calcule les composantes du vecteur direction
            direction_x = ((mouse_pos[0] - self.rect.x) * BULLET_SPEED) / SCREEN_WIDTH
            direction_y = ((mouse_pos[1] - self.rect.y) * BULLET_SPEED) / SCREEN_HEIGHT

            # [LEs composantes] Multipliées par la vitesse souhaitée
            speed_x = min(direction_x, BULLET_SPEED)
            speed_y = min(direction_y, BULLET_SPEED)
            self.shoot_time = pygame.time.get_ticks()
            # Créé et retourne la nouvelle balle
            return Bullet(self.damage, speed_x, speed_y, self.rect.center, self.currentLevel, True)

    # Trace le joueur
    def draw(self, screen):
        screen.blit(self.image, self.rect)
