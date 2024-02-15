import pygame
from matplotlib import animation

pygame.init()


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
        self.animation_cooldown = 100
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

    def draw(self, orientation = None):
        self.screen.blit(self.sprite_animation_list[self.frame], self.coordinates)

        if orientation is not None: # on inverse l'image
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

        self.space_button = Animation(screen, width, height, 'Assets/menu/space_button/space_button_spritesheet.png', 2, 64, 16,
                                      (x + box_width - 175, y + box_height- 50 ))

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

    def close(self):
        if self.active_dialogue == len(self.lines) - 1 and self.done:
            self.run = False
    # on arrête l'animation si toutes les lignes de texte ont été affichées


class Player:
    class Object:
        can = True
        x = 0
        y = 0

        def __init__(self, pos_x, pos_y, mass, friction_coef, max_speed, walk_speed, screen, scale) -> None:
            self.run_animation = None
            self.walk_animation = None
            self.jump_animation = None
            self.jump_animation2 = None
            self.run_attack_animation = None
            self.protect_animation = None
            self.hurt_animation = None
            self.defend_animation = None
            self.dead_animation = None
            self.attack1_animation = None
            self.attack2_animation = None
            self.attack3_animation = None
            self.idle_animation = None


            self.screen = screen
            self.scale = scale
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.pos = (self.pos_x, self.pos_y)
            self.mass = mass
            self.MaxSpeed = max_speed
            self.walk_speed = walk_speed
            self.FrictionCoef = friction_coef
            self.can_move = True
            self.speed_x = 0
            self.speed_y = 0
            self.speed = (0, 0)

        def init_animation(self,width,height_object, sheet_location, scale):
            self.run_animation = Animation(screen=self.screen, width=width, height=height_object,
                                           sheet_location=sheet_location, scale=scale, pixel_x=128, pixel_y=128,
                                           coordinates=(self.pos_x, self.pos_y))
            self.walk_animation = Animation(screen=self.screen, width=width, height=height_object,
                                           sheet_location=sheet_location, scale=scale, pixel_x=128, pixel_y=128,
                                           coordinates=(self.pos_x, self.pos_y))

        def mouvement(self) -> None:
            self.pos_x += self.speed_x
            self.pos_y += self.speed_y
            self.pos = (self.pos_x, self.pos_y)
            if self.can_move:
                if self.walk_speed <= self.speed_x < 0:
                    self.walk_animation.update()
                    self.walk_animation.draw(orientation= 'left')
                if  0 > self.speed_x <= self.walk_speed:
                    self.walk_animation.update()
                    self.walk_animation.draw()
            else:
                if self.speed_y > 0:
                    self.jump_animation.update()
                    self.jump_animation.draw()
                else:
                    self.jump_animation2.update()
                    self.jump_animation.draw()
        def strength(self, acceleration_x, acceleration_y) -> None:
            self.speed_x += acceleration_x
            self.speed_y += acceleration_y
            self.speed = (self.speed_x, self.speed_y)

        def show(self, surface, Screen) -> None:
            Screen.blit(surface, (self.pos_x, self.pos_y))