import pygame
from spritesheet import load_image, get_frame
from constants import GRAVITY, MAP_COLLISION_LAYER, SCREEN_HEIGHT, SCREEN_WIDTH

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Load the spritesheet for this player
        self.sprites = load_image("Assets/character/player/Player1.png")
        self.stillRight = get_frame(self.sprites, (0, 0, 48, 64))
        self.stillLeft = get_frame(self.sprites, (0, 64, 48, 64))

        # List of frames for each animation
        self.runningRight = (get_frame(self.sprites, (48, 0, 50, 64)),
                             get_frame(self.sprites, (102, 0, 50, 64)),
                             get_frame(self.sprites, (150, 0, 50, 64)),
                             get_frame(self.sprites, (251, 0, 50, 64)),
                             get_frame(self.sprites, (300, 0, 50, 64)),
                             get_frame(self.sprites, (354, 0, 50, 64)),
                             get_frame(self.sprites, (402, 0, 50, 64)))

        self.runningLeft = (get_frame(self.sprites, (48, 64, 50, 63)),
                            get_frame(self.sprites, (102, 64, 50, 63)),
                            get_frame(self.sprites, (150, 64, 50, 63)),
                            get_frame(self.sprites, (251, 64, 50, 63)),
                            get_frame(self.sprites, (300, 64, 50, 63)),
                            get_frame(self.sprites, (354, 64, 50, 63)),
                            get_frame(self.sprites, (402, 64, 50, 63)))

        self.jumpingLeft = \
            (get_frame(self.sprites, (61, 128, 50, 64)),
             get_frame(self.sprites, (107, 128, 50, 64)),
             get_frame(self.sprites, (156, 128, 50, 64)))

        self.jumpingRight = (get_frame(self.sprites, (49, 192, 48, 64)),
                             get_frame(self.sprites, (95, 192, 50, 64)),
                             get_frame(self.sprites, (156, 192, 50, 64)))

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
        difference_y, difference = 0, 0

        # Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - (SCREEN_WIDTH * 0.3):
            difference = -(self.rect.right - (SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)))
            self.rect.right = SCREEN_WIDTH - (SCREEN_WIDTH * 0.3)

        # Move screen is player reaches screen bounds
        if self.rect.left <= (SCREEN_WIDTH * 0.3):
            difference = (SCREEN_WIDTH * 0.3) - self.rect.left
            self.rect.left = (SCREEN_WIDTH * 0.3)

        # Move screen if player reaches screen bounds
        if self.rect.bottom >= SCREEN_HEIGHT - (SCREEN_WIDTH * 0.15):
            difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - (SCREEN_WIDTH * 0.15)))
            self.rect.bottom = SCREEN_HEIGHT - (SCREEN_WIDTH * 0.15)

        # Move screen is player reaches screen bounds
        if self.rect.top <= (SCREEN_WIDTH * 0.15):
            difference_y = (SCREEN_WIDTH * 0.15) - self.rect.top
            self.rect.top = (SCREEN_WIDTH * 0.15)
        self.currentLevel.shiftLevel(difference, difference_y)

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