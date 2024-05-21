import pytmx
import pygame
from constants import SCREEN_HEIGHT


class Level(object):
    def __init__(self, fileName):
        # Créer une carte/un niveau à partir de PyTMX
        self.mapObject = pytmx.load_pygame(fileName)
        self.map_height = self.mapObject.tileheight * (self.mapObject.height)
        self.map_width = self.mapObject.tilewidth * self.mapObject.width
        # Créer une liste des différentes "couches" (= "Calques" sur Tiled) de la carte
        self.layers = []

        # Niveau de décalage gauche/droite
        self.levelShift = 0
        self.levelShifty = self.map_height - SCREEN_HEIGHT - self.mapObject.tileheight
        # Créer une couche/un calque pour chaque couche/calque de la carte
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

    # Déplacer le calque vers la gauche/droite
    def shiftLevel(self, shiftX, shiftY):
        self.levelShift += shiftX
        self.levelShifty += shiftY

        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX
                tile.rect.y += shiftY

    # Met à jour le calque
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)


class Layer(object):
    def __init__(self, index, mapObject):
        # Index des couches de la carte
        self.index = index

        # Créer un groupe de tuiles pour le calque
        self.tiles = pygame.sprite.Group()

        # Objet de carte de référence
        self.mapObject = mapObject
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
