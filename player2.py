import pygame
from constants import GRAVITY, MAP_COLLISION_LAYER, SCREEN_HEIGHT, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        from spritesheet import SpriteSheet2
        pygame.sprite.Sprite.__init__(self)

        # Load the spritesheet for this player
        self.sprites = SpriteSheet2("Assets/character/player/Player1.png")

        self.stillRight = self.sprites.image_at((0, 0, 48, 64))
        self.stillLeft = self.sprites.image_at((0, 64, 48, 64))

        # List of frames for each animation
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

        # Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Set speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"

        # Boolean to check if player is running, current running frame, and time since last frame change
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()

        # Players current level, set after object initialized in game constructor
        self.currentLevel = None
        self.difference = 0

        self.dashtime = pygame.time.get_ticks()
    def update(self):
        # Update player position by change
        self.rect.x += self.changeX

        # Get tiles in collision layer that player is now touching
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # Move player to correct side of that block
        for tile in tileHitList:
            if self.changeX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
        difference_y, self.difference = 0, 0

        # change la camera si le joueur atteint le bord droit de l'écran
        if ((self.rect.right >= SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)) and
                ((SCREEN_WIDTH - self.currentLevel.levelShift) < self.currentLevel.map_width)):

            self.difference = -(self.rect.right - (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)))
            self.rect.right = SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)

        # change la camera si le joueur atteint le bord gauche de l'écran
        elif (self.rect.left <= (SCREEN_WIDTH * 0.3)) and 0 > self.currentLevel.levelShift:

            self.difference = (SCREEN_WIDTH * 0.3) - self.rect.left
            self.rect.left = (SCREEN_WIDTH * 0.3)

        # change la camera si le joueur atteint le bord inferieur de l'écran
        if ((self.rect.bottom >= SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)) and
                ((self.currentLevel.map_height - self.currentLevel.levelShifty) < SCREEN_HEIGHT)):

            difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)))
            self.rect.bottom = SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.15)

        # change la camera si le joueur atteint le bord superieur de l'écran
        elif self.rect.top <= (SCREEN_HEIGHT * 0.15):
            difference_y = (SCREEN_HEIGHT * 0.15) - self.rect.top
            self.rect.top = (SCREEN_HEIGHT * 0.15)

        self.currentLevel.shiftLevel(self.difference, difference_y)

        # Update player position by change
        self.rect.y += self.changeY

        # Get tiles in collision layer that player is now touching
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        # If there are tiles in that list
        if len(tileHitList) > 0:
            # Move player to correct side of that tile, update player frame
            for tile in tileHitList:
                if self.changeY > 0:
                    self.rect.bottom = tile.rect.top
                    self.changeY = 1

                    if self.direction == "right":
                        self.image = self.stillRight
                    else:
                        self.image = self.stillLeft
                else:
                    self.rect.top = tile.rect.bottom
                    self.changeY = 0
        # If there are no tiles in that list
        else:
            # Update player change for jumping/falling and player frame
            self.changeY += GRAVITY
            if self.changeY > 0:
                if self.direction == "right":
                    self.image = self.jumpingRight[1]
                else:
                    self.image = self.jumpingLeft[1]

        # If player is on ground and running, update running animation
        if self.running and self.changeY == 1:
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

            self.changeY = -6

    def dash(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2
        if len(tileHitList) > 0:
            if (pygame.time.get_ticks() - self.dashtime) > 3000:
                if self.direction == "right":
                    self.changeX = 20
                else:
                    self.changeX = -20
                self.dashtime = pygame.time.get_ticks()
    # Move right

    def goRight(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tileHitList) > 0:
            self.direction = "right"
            self.running = True
            self.changeX = 3

    # Move left
    def goLeft(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tileHitList) > 0:
            self.direction = "left"
            self.running = True
            self.changeX = -3

    # Stop moving
    def stop(self):
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2

        if len(tileHitList) > 0:
            self.running = False
            self.changeX = 0

    # Draw player
    def draw(self, screen):
        screen.blit(self.image, self.rect)
