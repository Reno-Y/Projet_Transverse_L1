import pygame
import pytmx
from pygame import surface
from function import *

pygame.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
MAP_COLLISION_LAYER = 0


class Spritesheet:
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, image_width, image_height, scale, color):
        image = pygame.Surface((image_width, image_height)).convert_alpha()
        image.blit(self.sheet, (0, 0), (frame * image_width, 0, image_width, image_height))
        image = pygame.transform.scale(image, (image_width * scale, image_height * scale))
        image.set_colorkey(color)
        return image
    # on récupère une image dans une spritesheet


class TittleName:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        title_image = pygame.image.load('Assets/menu/Chronicles_of_Etheria.png').convert_alpha()
        self.title_image = pygame.transform.scale(title_image, (self.width, self.height))
        # on charge l'image du titre et on la redimensionne

    def draw(self):
        self.screen.blit(self.title_image, (0, 0))
        # on affiche l'image du titre


class Music:
    def __init__(self, music_location):
        self.soundtrack = pygame.mixer.Sound(music_location)

    def play(self, loop):
        self.soundtrack.play(loop)
    # on joue la musique en boucle


class Animation:
    def __init__(self, screen, width, height, sheet_location, scale, pixel_x, pixel_y, coordinates):
        self.screen = screen
        self.width = width
        self.height = height
        self.sheet_location = sheet_location
        self.coordinates = coordinates
        sprite_sheet = pygame.image.load(sheet_location).convert_alpha()
        sheet_length = sprite_sheet.get_width()
        animation_step = sheet_length // pixel_x
        self.sprite = Spritesheet(sprite_sheet)
        self.sprite_animation_list = []
        self.sprite_animation_steps = animation_step
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 150
        self.frame = 0

        for i in range(animation_step):
            self.sprite_animation_list.append(
                self.sprite.get_image(i, pixel_x, pixel_y, scale, (0, 255, 246)))
            # On récupère les images de l'animation par leurs formats
            # On génère une liste d'images pour l'animation

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_update >= self.animation_cooldown:
            self.last_update = current_time
            self.frame = (self.frame + 1) % len(self.sprite_animation_list)
            # on change de frame à chaque fois que le cooldown est atteint

    def draw(self, orientation=None):
        self.screen.blit(self.sprite_animation_list[self.frame], self.coordinates)

        if orientation is not None:  # on inverse l'image
            self.screen.blit(pygame.transform.flip(self.sprite_animation_list[self.frame], False, True),
                             self.coordinates)
        # on affiche la frame actuelle


class Button:
    def __init__(self, x, y, image, scale, screen, sheet, width, height):
        self.x = x
        self.y = y
        image_width = image.get_width()
        image_height = image.get_height()
        self.image = pygame.transform.scale(image, (int(image_width * scale), int(image_height * scale)))
        self.scale = scale
        self.screen = screen
        self.sheet = sheet
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.width = width
        self.height = height
        self.button_animation = Animation(screen, width, height, sheet, scale, 64, 16,
                                          (x, y))

    def clicked(self):

        if self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0] == 1:
            # on vérifie si le bouton est cliqué

            return True

    def draw(self):
        pos = pygame.mouse.get_pos()  # on récupère la position de la souris

        if self.rect.collidepoint(pos):
            self.button_animation.update()
            self.button_animation.draw()
            # on affiche l'animation du bouton si la souris est dessus

        elif not self.rect.collidepoint(pos):
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
            # on affiche l'image du bouton si la souris n'est pas dessus


class Dialogue:
    def __init__(self, screen, height, width, box_width, box_height, x, y, text, color):
        self.text_surfaces = []  # on stocke les surfaces de texte pour les afficher sans animation
        self.screen = screen
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font('Assets/font/Pixeled.ttf', 15)
        self.rect = pygame.Rect(x, y, box_width, box_height)
        self.counter = 0
        self.speed = 1
        self.active_dialogue = 0
        self.lines = text
        self.text = text[self.active_dialogue]
        self.done = False
        self.run = True

        for lines in self.lines:
            self.text_surfaces.append(self.font.render(lines, True, self.color))
            # on génère une surface pour chaque ligne de texte pour les afficher plus tard sans animation

        self.space_button = Animation(screen, width, height, 'Assets/menu/space_button/space_button_spritesheet.png', 2,
                                      64, 16,
                                      (x + box_width - 175, y + box_height - 50))

    def draw(self):
        if self.run:
            self.counter += self.speed
            text_surface = self.font.render(self.text[:self.counter], True, self.color)
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
            self.screen.blit(text_surface, (self.x + 20, self.y + 10 + 40 * self.active_dialogue))
            # on affiche le texte avec une animation de défilement

            for i in range(len(self.lines)):
                if i < self.active_dialogue:
                    self.screen.blit(self.text_surfaces[i], (self.x + 20, self.y + 10 + 40 * i))
                    # on affiche les lignes de texte déjà affichées sans animation

            if self.counter < len(self.text):
                self.counter += 1

                # on fait défiler le texte

            elif self.counter >= len(self.text):
                self.done = True
                self.space_button.draw()
                self.space_button.update()

                # on indique que l'animation est terminée
            self.text = self.lines[self.active_dialogue]
            # on récupère la ligne de texte correspondant à l'indice actif car le texte est slice par chaque caractère

    def skip(self):
        self.counter += 4
        if self.counter >= len(self.text):
            self.counter = len(self.text)
        # on fait défiler le texte plus rapidement si le joueur appuie sur la touche espace

    def next(self):

        if self.done and self.active_dialogue < len(self.lines) - 1:
            self.text = self.text[self.active_dialogue]
            self.active_dialogue += 1
            self.done = False
            self.counter = 0
        # on passe à la ligne de texte suivante si l'animation est terminée et qu'il reste des lignes de texte

    def closed(self):
        if self.active_dialogue == len(self.lines) - 1 and self.done:
            self.run = False
            return True
    # on arrête l'animation si toutes les lignes de texte ont été affichées


# -------------------------------------------------------------------#


class Level(object):
    def __init__(self, fileName):
        # Create map object from PyTMX
        self.mapObject = pytmx.load_pygame(fileName)

        # Create list of layers for map
        self.layers = []

        # Amount of level shift left/right
        self.levelShift = 0

        # Create layers for each layer in tile map
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

    # Move layer left/right
    def shiftLevel(self, shiftX, shiftY):
        self.levelShift += shiftX
        self.levelShift += shiftY

        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX
                tile.rect.y += shiftY

    # Update layer
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


class Layer(object):
    def __init__(self, index, mapObject):
        # Layer index from tiled map
        self.index = index

        # Create gruop of tiles for this layer
        self.tiles = pygame.sprite.Group()

        # Reference map object
        self.mapObject = mapObject

        # Create tiles in the right position for each layer
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(Tile(image=img, x=(x * self.mapObject.tilewidth), y=(y * self.mapObject.tileheight)))

    # Draw layer
    def draw(self, screen):
        self.tiles.draw(screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Layer(object):
    def __init__(self, index, mapObject):
        # Layer index from tiled map
        self.index = index

        # Create gruop of tiles for this layer
        self.tiles = pygame.sprite.Group()

        # Reference map object
        self.mapObject = mapObject

        # Create tiles in the right position for each layer
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(Tile(image=img, x=(x * self.mapObject.tilewidth), y=(y * self.mapObject.tileheight)))

    # Draw layer
    def draw(self, screen):
        self.tiles.draw(screen)


class SpriteSheet2(object):
    def __init__(self, fileName):
        self.sheet = pygame.image.load(fileName)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        return image


class Game(object):
    def __init__(self):
        # Set up a level to load
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName="Assets/levels/level1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]
        self.move = False
        # Create a player object and set the level it is in
        self.player = Player(x=200, y=100)
        self.player.currentLevel = self.currentLevel


    def processEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            # Get keyboard input and move player accordingly
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_LEFT:
                    self.move = True
                    self.player.goLeft()
                elif event.key == pygame.K_RIGHT:
                    self.move = True
                    self.player.goRight()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT) and self.player.changeX < 0:
                    self.move = False
                if (event.key == pygame.K_RIGHT) and self.player.changeX > 0:
                    self.move = False
        if (self.move == False):
            self.player.stop()

        return True

    def runLogic(self):
        # Update player movement and collision logic
        self.player.update()

    # Draw level, player, overlay
    def draw(self, screen):
        screen.fill((135, 206, 235))
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Load the spritesheet of frames for this player
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
        if self.rect.right >= SCREEN_WIDTH - 200:
            difference = -(self.rect.right - (SCREEN_WIDTH - 200))
            self.rect.right = SCREEN_WIDTH - 200

        # Move screen is player reaches screen bounds
        if self.rect.left <= 200:
            difference = 200 - self.rect.left
            self.rect.left = 200

        # Move screen if player reaches screen bounds
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - 50))
            self.rect.bottom = SCREEN_HEIGHT - 50

        # Move screen is player reaches screen bounds
        if self.rect.top <= 100:
            difference_y = 100 - self.rect.top
            self.rect.top = 100
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
        # If there are not tiles in that list
        else:
            # Update player change for jumping/falling and player frame
            self.changeY += 0.2
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
        if pygame.time.get_ticks() - self.runningTime > 50:
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


class PauseMenu:

    def __init__(self):
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((width, height))
        self.start_button = pygame.image.load('Assets/menu/start/start2.png').convert_alpha()
        self.button_width, self.button_height = self.start_button.get_rect().width, self.start_button.get_rect().height
        self.clock = pygame.time.Clock()

        self.resume_button = pygame.image.load('Assets/menu/resume/resume1.png').convert_alpha()
        self.resume_button = Button((width / 2 - self.button_width * 3.5 / 2), (height / 2 - (self.button_height * 3.5) * 1.5),
                                    self.resume_button, 3.5, screen, 'Assets/menu/resume/resume_spritesheet.png', width,
                                    height)

        self.quit_button = pygame.image.load('Assets/menu/quit/quit1.png').convert_alpha()
        self.quit_button = Button((width / 2 - self.button_width * 3.5 / 2), (height / 2 + (self.button_height * 3.5 / 2) * 3),
                                  self.quit_button,
                                  3.5, screen, 'Assets/menu/quit/quit_spritesheet.png', width, height)
        self.setting_button = pygame.image.load('Assets/menu/settings/settings1.png').convert_alpha()
        self.setting_button = Button((width / 2 - self.button_width * 3.5 / 2), (height / 2 + self.button_height * 3.5 / 2),
                                     self.setting_button,
                                     3.5, screen, 'Assets/menu/settings/settings_spritesheet.png', width, height)
        self.main_menu_button = pygame.image.load('Assets/menu/main_menu/main_menu_1.png').convert_alpha()
        self.main_menu_button = Button((width / 2 - self.button_width * 3.5 / 2), (height / 2 - self.button_height * 3.5 / 2),
                                       self.main_menu_button,
                                       3.5, screen, 'Assets/menu/main_menu/main_menu_spritesheet.png', width, height)

        self.screen = pygame.display.set_mode((width, height))
        self.inf = 0
        self.scroll = 0

    def run_pause_menu(self,boolean):

        run = boolean
        inf = 0
        scroll = 0
        bg_images = parallax_init("assets/background/sunset_sky")
        while run:
            screen.fill((0, 0, 0))  # remplissage de l'écran
            inf += 1
            parallax(scroll, bg_images)
            scroll += 2

            self.quit_button.draw()
            self.setting_button.draw()
            self.resume_button.draw()
            self.main_menu_button.draw()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False

                if self.quit_button.clicked():
                    quit()

                if self.resume_button.clicked():
                    run = False

                if self.main_menu_button.clicked():
                    # run_menu(True)
                    run = False

            clock.tick(60)
            pygame.display.update()
