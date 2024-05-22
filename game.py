from music import Music
from bullet import Bullet
from function import *
from player import Player
from tiles_map import *
from pause_menu import PauseMenu
from enemie import Enemies
from gameover import GameOver
pygame.init()
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
MAP_COLLISION_LAYER = 0
GameOver = GameOver(screen)

music = Music("sound/music/voyage.mp3")
death_sound = Music("sound/effect/deathsound.mp3")

# -------------------------------------------------------------------#


class Game(object):
    def __init__(self, list_player_pos, level_directory, list_enemies):
        # Définit un niveau à charger
        self.scroll = 310
        self.bg_images = parallax_init("assets/background/level0")
        self.currentLvNb = 0
        self.pause = PauseMenu(screen)
        self.levels = load_levels(level_directory)
        self.currentLevel = self.levels[self.currentLvNb]
        self.move = False
        # Créer l'objet joueur et positionne celui-ci dans le niveau défini
        self.player = Player(list_player_pos[self.currentLvNb])
        self.player_group = pygame.sprite.Group(self.player)
        self.list_player_pos = list_player_pos
        self.player.currentLevel = self.currentLevel
        self.player.rect.y += (SCREEN_HEIGHT - self.currentLevel.map_height - self.player.rect.height)
        self.list_enemies = list_enemies
        self.bullets = pygame.sprite.Group()
        self.enemies = Enemies(list_enemies[self.currentLvNb], self.currentLevel, self.player_group, self.bullets,
                               self.player)
        Bullet.player_group = self.player_group
        Bullet.enemies = self.enemies.enemies_group
        self.move_left = False
        self.move_right = False

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            # Récupère les inputs du clavier et déplace le joueur en fonction de ceux-ci
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.pause.run(True):
                        music.soundtrack.stop()
                        return "main_menu"
                elif event.key == pygame.K_LEFT:
                    self.move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.move_right = True
                elif event.key == pygame.K_UP:
                    self.player.jump()
                elif event.key == pygame.K_w:
                    self.player.dash()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.move_left = False
                if event.key == pygame.K_RIGHT:
                    self.move_right = False

            if pygame.mouse.get_pressed()[0]:
                bullet = self.player.shoot(pygame.mouse.get_pos())
                if bullet is not None:
                    self.bullets.add(bullet)

        if not self.move_right and not self.move_left:
            self.player.stop()
        else:
            if self.move_left:
                self.player.go_left()
            if self.move_right:
                self.player.go_right()

        if (self.player.rect.x > SCREEN_WIDTH) and (len(self.enemies.enemies_group) == 0):  # scene suivante
            if len(self.levels) > self.currentLvNb + 1:
                self.currentLvNb += 1
                self.currentLevel = self.levels[self.currentLvNb]
                self.player.currentLevel = self.currentLevel
                self.bullets.empty()
                if len(self.list_player_pos) > self.currentLvNb:
                    self.player.rect.x = self.list_player_pos[self.currentLvNb][0]
                    self.player.rect.y = self.list_player_pos[self.currentLvNb][1]
                else:
                    self.player.rect.x = 128
                    self.player.rect.y = 279
                    self.player.speedY = 0
                    self.player.speedX = 0
                if len(self.list_enemies) > self.currentLvNb:
                    self.enemies.next_level(self.list_enemies[self.currentLvNb], self.currentLevel, self.player_group,
                                            self.bullets, self.player)
                    Bullet.enemies = self.enemies.enemies_group
                else:
                    self.enemies.enemies_group.empty()
                    Bullet.enemies = None
            else:
                music.soundtrack.stop()
                return False
        elif (self.player.rect.right > SCREEN_WIDTH) and (len(self.enemies.enemies_group) > 0):
            self.player.rect.right = SCREEN_WIDTH
        if self.player.rect.y > SCREEN_HEIGHT or self.player.life <= 0:
            music.soundtrack.stop()  # Game over
            death_sound.play(0)
            GameOver.run(True)

            return "main_menu"

        return True

    def run_logic(self):
        # Met à jour le mouvement du joueur et les collisions
        self.player.update()
        self.enemies.update()
        self.bullets.update()
        self.scroll += 2 - self.player.difference

    #  Préparation du niveau, du joueur, et de l'overlay

    def draw(self):
        screen.fill((135, 206, 235))
        parallax(self.scroll, self.bg_images, screen)
        self.currentLevel.draw(screen)
        self.bullets.draw(screen)
        self.enemies.draw(screen)
        self.player.draw(screen)
        pygame.display.flip()

    def music(self):
        music.play(-1)
        # music.play(-1) permet de jouer la musique en boucle


def load_levels(levels_directory):
    levels = []
    for file_name in os.listdir(levels_directory):
        if file_name.endswith(".tmx"):
            level_path = os.path.join(levels_directory, file_name)
            levels.append(Level(file_name=level_path))
    return levels
