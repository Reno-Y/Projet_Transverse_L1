from function import *
import pygame as pg
from animation import Animation
#TODO: export utility and delete file
infini = True
Lanceur = True

clock = pg.time.Clock()

SCREEN_WIDTH = pygame.display.Info().current_w  # Récupération de la largeur de l'écran
SCREEN_HEIGHT = pygame.display.Info().current_h  # Récupération de la hauteur de l'écran

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

movement_right = False
movement_left = False

"""
Appel des animations du joueur et des monstres
"""

Player_idle_left = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                             'Assets/character/player/Idle_gauche.png', 1.2, 128, 128,
                             (0, 0))
Player_idle_right = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                              'Assets/character/player/idle_droite.png', 1.2, 128, 128,
                              (0, 0))
# SEQUENCE_IM_joueur court_/gauche/droite
Player_run_left = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                            'Assets/character/player/Run_gauche.png', 1.2, 128, 128,
                            (0, 0))
Player_run_right = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                             'Assets/character/player/Run_droite.png', 1.2, 128, 128,
                             (0, 0))
# SEQUENCE_IM_joueur frappe1_/gauche/droite
Player_attack_left = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                               'Assets/character/player/Attack_gauche.png', 1.2, 128, 128,
                               (0, 0))
Player_attack_right = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                'Assets/character/player/Attack_droite.png', 1.2, 128, 128,
                                (0, 0))
# SEQUENCE_IM_joueur frappe2_/gauche/droite
Player_attack2_left = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                'Assets/character/player/Attack2_gauche.png', 1.2, 128, 128,
                                (0, 0))
Player_attack2_right = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                 'Assets/character/player/Attack2_droite.png', 1.2, 128, 128,
                                 (0, 0))
# SEQUENCE_IM_joueur defense_/gauche/droite
Player_defense_left = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                'Assets/character/player/Defense_gauche.png', 1.2, 128, 128,
                                (0, 0))
Jo_defense_d = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                         'Assets/character/player/Defense_droite.png', 1.2, 128, 128,
                         (0, 0))
# SEQUENCE_IM_joueur defense.attaque_/gauche/droite
Player_defence_left = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                'Assets/character/player/DefAttack_gauche.png', 1.2, 128, 128,
                                (0, 0))
Player_defence_right = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                                 'Assets/character/player/DefAttack_droite.png', 1.2, 128, 128,
                                 (0, 0))





class Player():
    def __init__(self):
        self.pos_x = 0
        self.pos_y = 0
        self.pos = [self.pos_x, self.pos_y]
        self.speed_x = 0
        self.speed_y = 0
        self.speed = [self.speed_x, self.speed_y]
        self.hitbox_width = 50
        self.hitbox_height = 50
        self.mass = 10
        self.max_speed = 2  # Definie la vitesse de deplacement max du joueur
        self.life = 30000  # Definie les points de vie du joueur
        self.statut = 0
        self.attack_range = 130  # Definie la portee des attaques
        self.strenght = [50,0]  # Definie les degats causes par les attaques du joueurs, et si celle-ci affligent des status
        self.size = [128, 128]
        self.scale = 1.2

        self.FrictionCoef = 0

        # Variable definissant l'action actuellement effectue par le joueur
        # [X, 0, 0, 0, 0] définie la direction du mouvement, avec 0 immobile, 1 haut, 2 bas, 3 gauche, 4 droite
        # [0, X, 0, 0, 0] définit l'intensité du mouvement, par exemple si le joueur est immobile, marche, ou court
        # [0, 0, X, 0, 0] définit l'action effectue, par exemple frapper, se guerir, interagir
        # [0, 0, 0, X, 0] sert de souvenir, en recuperant la derniere inclinaison
        # [0, 0, 0, 0, X] sert de souveni, en definissant le statut du joueur relatif au combat, ici 0 neutre, 1 invulnerable due a des dommages subis, 2 invulnerable due a des facteurs exterieurs

        self.action = [0, 0, 0, 0, 0]
        self.rect = pg.Rect(self.pos_x, self.pos_y, self.size[0], self.size[1])
        self.currentLevel = None

    def regard_statut(self, marked_zone):

        life = self.life

        # Dans le cas où le joueur se retrouve au sein d'une zone marquee, on applique les instructions donnees par la zone

        for x in range(len(marked_zone)):
            if self.pos_x > marked_zone[x][0] and self.pos_x <= marked_zone[x][2] and self.pos_y > marked_zone[x][
                1] and self.pos_y <= marked_zone[x][3] and self.action[4] == 0:
                # Si definie, inflige/octroie des points de vie
                self.life -= marked_zone[x][4][0]
                if self.life < life:
                    self.action[1] == 1
            elif self.life <= 0:
                self.action[1] == 1
                infini = False
                return infini

            self.statut = marked_zone[x][4][1]  # Si definie, herite un statut au joueur

    def movement_action(self, pos_cam):

        pos_x = pos_cam[0]
        pos_y = pos_cam[1]

        # Recup l'input clavier
        ClavIn = pg.key.get_pressed()


        # Mouvement_GAUCHE
        if ClavIn[pg.K_q] and ClavIn[pg.K_k] == False:
            self.speed_x -= self.max_speed
            pos_x += self.max_speed
            self.action[0] = 3
            self.action[3] = 1

        # Mouvement_DROITE
        if ClavIn[pg.K_d] and ClavIn[pg.K_k] == False:
            self.speed_x += self.max_speed
            pos_x -= self.max_speed
            self.action[0] = 4
            self.action[3] = 0

        # CONTROLE_SortieDeMap

        # LIMITE_frontiere (Elements interieurs exclus)
        up_lim_x = SCREEN_WIDTH - self.hitbox_width * 2
        bot_lim_x = 0 - self.hitbox_width
        sup_lim_y = SCREEN_HEIGHT - self.hitbox_height * 3
        bot_lim_y = 0 - self.hitbox_height * 1.5

        if self.pos_x < bot_lim_x:
            self.pos_x = bot_lim_x
            pos_x = pos_cam[0]
        elif self.pos_x > up_lim_x:
            self.pos_x = up_lim_x
            pos_x = pos_cam[0]

        if self.pos_y < bot_lim_y:
            self.pos_y = bot_lim_y
            pos_y = pos_cam[1]
        elif self.pos_y > sup_lim_y:
            self.pos_y = sup_lim_y
            pos_y = pos_cam[1]

        # ACTION_joueur
        # ACT_ATTAQUE
        if ClavIn[pg.K_j]:
            # ATTAQUER
            self.action[2] = 1
            marked_zone_left = [self.pos_x - self.attack_range - 5, self.pos_y - self.attack_range - 5, self.pos_x - 5,
                    self.pos_y + 50,
                    self.strenght]
            marked_zone_left = [self.pos_x + 5, self.pos_y - 50, self.pos_x + self.attack_range + 5,
                    self.pos_y + self.attack_range + 5,
                    self.strenght]
            # On determine le sens de l'attaque, pour definir correctement la zone marquee
            if self.action[3] == 1:  # GAUCHE
                Debut(marked_zone_left)
            else:  # DROITE
                Debut(marked_zone_left)

        # ACT_DEFENSE
        if ClavIn[pg.l]:
            # SE DEFENDRE
            self.action[2] = 2
        # ACT_RUEE
        if ClavIn[pg.K_LEFT] and ClavIn[pg.K_k]:
            # SE RUE EN AVANT
            self.speed_x -= self.max_speed * 10
            pos_x += self.max_speed * 10
            self.action[0] = 3
            self.action[3] = 1

        if ClavIn[pg.K_RIGHT] and ClavIn[pg.K_KP4]:
            # SE RUE EN AVANT
            self.speed_x += self.max_speed * 10
            pos_x -= self.max_speed * 10
            self.action[0] = 4
            self.action[3] = 0

        return (pos_x, pos_y)

    # Affiche le sprite du joueur, en prenant en compte le mouvement effectue
    """"
    def update(self):
        self.rect.x += self.speed_x
        tileHitList = pg.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        # Move player to correct side of that block
        for tile in tileHitList:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
        difference_y, difference = 0, 0
        # Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - SCREEN_WIDTH // 10:
            difference = -(self.rect.right - (SCREEN_WIDTH // 10))
            self.rect.right = SCREEN_WIDTH - SCREEN_WIDTH // 10

        if self.rect.left <= SCREEN_WIDTH // 10:
            difference = SCREEN_WIDTH // 10 - self.rect.left
            self.rect.left = SCREEN_WIDTH // 10

        if self.rect.bottom >= SCREEN_HEIGHT - SCREEN_WIDTH // 40:
            difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - SCREEN_WIDTH // 40))
            self.rect.bottom = SCREEN_HEIGHT - (SCREEN_WIDTH // 40)

        if self.rect.top <= SCREEN_WIDTH // 20:
            difference_y = SCREEN_WIDTH // 20 - self.rect.top
            self.rect.top = SCREEN_WIDTH // 20
        self.currentLevel.shiftLevel(difference, difference_y)

        self.rect.y += self.speed_y  # Update player position

        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        if len(tileHitList) > 0:
            for tile in tileHitList:
                if self.speed_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.speed_y = 1
                    # TODO: refait les annimation
                #                    if self.direction == "right":
                #                        self.image = self.stillRight
                #                    else:
                #                         self.image = self.stillLeft
                else:
                    self.rect.top = tile.rect.bottom
                    self.speed_y = 0
        else:
            # Update player change for jumping/falling and player frame
            self.speed_y += 0.2
            #            if self.speed_y > 0:
            # TODO: refait les annimation
            #                if self.direction == "right":
            #                    self.image = self.jumpingRight[1]
            #                else:
            #                    self.image = self.jumpingLeft[1]
            # If player is on ground and running, update running animation

            if self.running and self.changeY == 1:
                if self.direction == "right":
                    self.image = self.runningRight[self.runningFrame]
                else:
                    self.image = self.runningLeft[self.runningFrame]
            
        #When correct amount of time has passed, go to next frame
        if pygame.time.get_ticks() - self.runningTime > 50:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1        
   """

    def draw(self):

        # Dessine une barre de vie
        pg.draw.rect(screen, (255, 0, 0), (50, 100, 70, 35))
        pg.draw.rect(screen, (0, 128, 0), (50, 100, 20 - (5 * (10 - self.life // 400)), 35))

        # Action_AVANT
        if self.action[0] == 1:
            Player_run_right.draw((self.pos_x, self.pos_y))
            Player_run_right.update()
            self.action[0] = 0

        # Action_ARRIERE
        elif self.action[0] == 2:
            Player_run_left.draw((self.pos_x, self.pos_y))
            Player_run_left.update()
            self.action[0] = 0

        # Action_GAUCHE
        elif self.action[0] == 3:
            if self.action[2] == 1:
                Player_defence_left.draw((self.pos_x, self.pos_y))
                Player_defence_left.update()
                self.action[0] = 0
                self.action[2] = 0
            # elif self.action[2] == 3: EN ATTENTE, manque animation "dash", soit celle de la ruee

            else:
                Player_run_left.draw((self.pos_x, self.pos_y))
                Player_run_left.update()
                self.action[0] = 0

        # Action_DROITE
        elif self.action[0] == 4:
            if self.action[2] == 1:
                Player_defence_right.draw((self.pos_x, self.pos_y))
                Player_defence_right.update()
                self.action[0] = 0
                self.action[2] = 0
            else:
                Player_run_right.draw((self.pos_x, self.pos_y))
                Player_run_right.update()
                self.action[0] = 0

        # Action_IMMOBILE
        else:
            if self.action[2] == 1:  # ATTAQUE
                if self.action[3] == 1:
                    Player_attack_left.draw((self.pos_x, self.pos_y))
                    Player_attack_left.update()
                    self.action[2] = 0
                else:
                    Player_attack_right.draw((self.pos_x, self.pos_y))
                    Player_attack_right.update()
                    self.action[2] = 0

            elif self.action[2] == 2:  # DEFENSE
                if self.action[3] == 1:
                    Player_defense_left.draw((self.pos_x, self.pos_y))
                    Player_defense_left.update()
                    self.action[2] = 0
                else:
                    Jo_defense_d.draw((self.pos_x, self.pos_y))
                    Jo_defense_d.update()
                    self.action[2] = 0

            else:
                if self.action[3] == 1:
                    Player_idle_left.draw((self.pos_x, self.pos_y))
                    Player_idle_left.update()
                else:
                    Player_idle_right.draw((self.pos_x, self.pos_y))
                    Player_idle_right.update()




class ZONE_MARQUEE:
    def __init__(self, pos_1_x, pos_1_y, pos_2_x, pos_2_y, force):
        self.pos_1_x = pos_1_x  # ^ Y
        self.pos_1_y = pos_1_y  # |
        self.pos_2_x = pos_2_x  # |
        self.pos_2_y = pos_2_y  # (x,y) |-> X   [x, y, X, Y, causalité(degat/soint, statut)] organisation de "zonemarquee"
        # |
        # Relai a "force"
        self.force = force
        # |
        self.archive = []


def Debut(zm):
    ZoneMarquee_monde1.archive.append(zm)


def Fin():
    ZoneMarquee_monde1.archive = ZoneMarquee_monde1.archive.pop(0)


# CREATION_ZoneMarquee_relatif_monde1
ZoneMarquee_monde1 = ZONE_MARQUEE(9999, 9999, 9999, 9999, [9999, 9999])




















""""

def MAIN_appelINFINI(Afficheur, compte):



    Jo = JOUEUR()
    Mo_slim1 = MONSTRE(1000, 300, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    Mo_slim2 = MONSTRE(1500, 50, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    Mo_slim3 = MONSTRE(2000, 200, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    Mo_slim4 = MONSTRE(1700, 250, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    list_slim = [Mo_slim1, Mo_slim2, Mo_slim3, Mo_slim4]


    pos_cam = [500, 500]
   
   
    Separateur = 1

    while infini:
        compte.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None

        # Permet de separer en 2 "monde"
        Separateur = -Separateur

        # |
        pos_cam = Jo.movement_action(pos_cam)
        # |
        for Slim in list_slim:
            Slim.PatrouilleRecherche((Jo.pos_x, Jo.pos_y))

        if ZoneMarquee_monde1.archive != []:
            Jo.regard_statut(ZoneMarquee_monde1.archive)

            for Slim in list_slim:
                Slim.regard_statut(ZoneMarquee_monde1.archive)
            ZoneMarquee_monde1.archive = []

        # |
        ECran_afficheur.fill(WHITE)
        # |
        screen.fill(BLACK)
        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
        # RENDU_MAP
        screen.blit(image_mapV6, (0, 0))  # image_colE1_pP
        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
        # |
        for x in range(10):
            pg.draw.rect(screen, BLUE, ((x * 100, x * 100), (20, 20)))

        # --|
        # RENDU_Monstre
        # RENDU_BOSS
        screen.blit(Boss_inc, (1300, 850))
        # RENDU_Monstre
        # Monde.blit(im_monstreTest, (Mo.pos_x, Mo.pos_y))

        for Slim in list_slim:
            Slim.rendu(screen)

        # -|
        # RENDU_Joueur
        Jo.rendu(screen)

        # -|
        # RENDU_FONDMonde
        ECran_afficheur.blit(screen, pos_cam)
        # --|
        # Monde.blit(image_colE1_pA, (0, 200))

        # |

        # |

        pg.display.flip()


# PROPAGATEUR_lineaire

    MAIN_appelINFINI(ECran_afficheur, clock)
"""