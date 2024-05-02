import json
import math
import random
import time
import os

import pygame


class TilesMap:
    def __init__(self, size_map, view_size):
        self.size_map = size_map
        self.view_size = view_size
        self.tile_map = None
        self.tiles_map_layers = None
        self.tiles_type = {}

    def load_map(self, path):
        f = open(path, 'r')
        dat = f.read()
        f.close()
        json_dat = json.loads(dat)
        self.tile_map = json_dat['map']
        self.tiles_map_layers = json_dat['layers']

    def clean(self):
        self.tile_map = None
        self.tiles_map_layers = None


    def load_tiles(self):
        for layer in self.tiles_map_layers:

    def init_tiles_type(self):
        dirs = os.listdir("Assets/map")
        for file in dirs:
            self.tiles_type[file](pygame.image.load(os.path.join('Assets/map/', file)).convert_alpha())