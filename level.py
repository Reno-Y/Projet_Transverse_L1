import pygame
from game import Game
from animation import Animation
from constants import FPS, SCREEN_HEIGHT, SCREEN_WIDTH

width, height = SCREEN_WIDTH, SCREEN_HEIGHT
screen = pygame.display.set_mode((width, height))

player_location = [width / 4, height / 1.8]
player_idle = Animation(screen, width, height, 'Assets/character/player/idle.png', 2.4, 128, 128,
                        player_location)
player_run = Animation(screen, width, height, 'Assets/character/player/Run.png', 2.4, 128, 128,
                       player_location)


def run_level1(boolean):
    game = Game([(32, 279)], "Assets/levels/", [
        [(1280, 256), (1280, 64)],
        [],
        [(1152, 288), (1472, 384), (1888, 352), (2080, 224), (1280, 480), (1696, 480)],
        [(928, 512), (1024, 544), (1216, 512), (1248, 480), (1280, 448), (1344, 512), (1408, 480), (2080, 256)],
        [(256, 310), (432, 465), (688, 496), (1056, 496), (1376, 527), (1664, 496), (1792, 496), (2176, 310),
         (2336, 403)],
        [(352, 496), (640, 403), (800, 155), (1056, 186), (1184, 310), (1376, 217), (1504, 341), (1504, 527),
         (1616, 310), (1984, 155), (2208, 465), (2368, 403)],
        [(832, 416), (1088, 544), (752, 224), (624, 288), (1328, 512), (1440, 480), (1504, 448), (1664, 416),
         (1632, 192), (1776, 224), (2144, 192), (2080, 160)],
        [(176, 32), (320, 224), (384, 192), (560, 32), (832, -32), (800, 160), (1056, 256), (1136, 224), (1248, 320),
         (1376, 320), (1312, 544), (1696, 448), (1824, 384), (1920, 320), (1568, 192)]])

    game.music()

    while boolean:

        state = game.process_events()
        if state == "main_menu":
            return "main_menu"
        else:
            boolean = state
        game.runLogic()
        game.draw()

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    return boolean
