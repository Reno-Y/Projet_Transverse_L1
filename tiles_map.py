import pytmx
import pygame
from constants import SCREEN_HEIGHT


class Level(object):
    def __init__(self, file_name):
        # Créer une carte/un niveau à partir de PyTMX
        self.mapObject = pytmx.load_pygame(file_name)
        self.map_height = self.mapObject.tileheight * self.mapObject.height
        self.map_width = self.mapObject.tilewidth * self.mapObject.width
        # Créer une liste des différentes "couches" (= "Calques" sur Tiled) de la carte
        self.layers = []

        # Niveau de décalage gauche/droite
        self.levelShift = 0
        self.levelShifty = self.map_height - SCREEN_HEIGHT - self.mapObject.tileheight
        # Créer une couche/un calque pour chaque couche/calque de la carte
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, map_object=self.mapObject))

    # Déplacer le calque vers la gauche/droite
    def shift_level(self, shift_x, shift_y):
        self.levelShift += shift_x
        self.levelShifty += shift_y

        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shift_x
                tile.rect.y += shift_y

    # Met à jour le calque
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


class Layer(object):
    def __init__(self, index, map_object):
        # Index des couches de la carte
        self.index = index

        # Créer un groupe de tuiles pour le calque
        self.tiles = pygame.sprite.Group()

        # Objet de carte de référence
        self.mapObject = map_object
        self.map_height = self.mapObject.tileheight * (self.mapObject.height + 1)

        # Créer des tuiles dans la bonne position pour chaque couche
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(Tile(image=img, x=(x * self.mapObject.tilewidth),
                                        y=(y * self.mapObject.tileheight) + (SCREEN_HEIGHT - self.map_height)))

    # Dessine le calque
    def draw(self, screen):

        self.tiles.draw(screen)


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
