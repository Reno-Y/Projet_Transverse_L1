from pygame import display, init

init()
# constantes
SCREEN_WIDTH = display.Info().current_w
SCREEN_HEIGHT = display.Info().current_h
FPS = 60

BUTTON_SCALE = 0.15

# constantes de la physique
MAP_COLLISION_LAYER = 0
GRAVITY = 0.2

# constantes du joueur
PLAYER_AIRMOVE = False
PLAYER_SPEED = 3
PLAYER_DOMAGE = 1
PLAYER_LIFE = 10

# constantes des balles
BULLET_SPEED = 30
BULLET_SCALE = 2


ENEMIE_SCALE = 6
