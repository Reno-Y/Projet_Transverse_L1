import pytmx
import pygame
from constants import SCREEN_HEIGHT


class Level(object):
    def __init__(self, fileName):
        # Create map object from PyTMX
        self.mapObject = pytmx.load_pygame(fileName)
        self.map_height = self.mapObject.tileheight * (self.mapObject.height)
        self.map_width = self.mapObject.tilewidth * self.mapObject.width
        # Create list of layers for map
        self.layers = []

        # Amount of level shift left/right
        self.levelShift = 0
        self.levelShifty = self.map_height - SCREEN_HEIGHT - self.mapObject.tileheight
        # Create layers for each layer in tile map
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index=layer, mapObject=self.mapObject))

    # Move layer left/right
    def shiftLevel(self, shiftX, shiftY):
        self.levelShift += shiftX
        self.levelShifty += shiftY

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

        # Create group of tiles for this layer
        self.tiles = pygame.sprite.Group()

        # Reference map object
        self.mapObject = mapObject
        self.map_height = self.mapObject.tileheight * (self.mapObject.height+1)

        # Create tiles in the right position for each layer
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    self.tiles.add(Tile(image=img, x=(x * self.mapObject.tilewidth),
                                        y=(y * self.mapObject.tileheight) + (SCREEN_HEIGHT - self.map_height)))

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


