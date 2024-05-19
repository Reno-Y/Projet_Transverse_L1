import pygame
import pytmx
from pygame import surface

from bullet import Bullet
from function import *
from player2 import Player
from tiles_map import *

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
        self.bullets = pygame.sprite.Group()

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
