from pygame import display, init

init()

# constantes d'affichage
BUTTON_SCALE = 0.15
SCREEN_WIDTH = display.Info().current_w
SCREEN_HEIGHT = display.Info().current_h
FPS = 60

# constantes de la physique
MAP_COLLISION_LAYER = 0
GRAVITY = 0.2

# constantes du joueur
PLAYER_AIR_MOVE = False
PLAYER_DASH = True
PLAYER_DASH_DELAY = 2000  # temps en ms
PLAYER_SHOOT_DELAY = 2000  # temps en ms
PLAYER_SPEED = 3
PLAYER_DAMAGE = 1
PLAYER_LIFE = 10
PLAYER_JUMP_ACCELERATION = -6

# constantes des balles
BULLET_SPEED = 30
BULLET_SCALE = 2

# constantes de l'ennemie
ENEMIES_SCALE = 6
ENEMIES_DAMAGE = 2
ENEMIES_LIFE = 3
ENEMIES_ATTACK_DELAY = 1000  # temps en ms
