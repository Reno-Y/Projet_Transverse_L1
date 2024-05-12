from Class import Animation
from function import *


class Player:

    def __init__(self, pos_x, pos_y, screen, scale) -> None:
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
        self.mass = 10
        self.MaxSpeed = 30
        self.walk_speed = 20
        self.FrictionCoef = 0.9
        self.can_move = True
        self.speed_x = 0
        self.speed_y = 0
        self.speed = (0, 0)
        self.level = None

    def init_animation(self, width, height_object, sheet_location, scale):
        self.run_animation = Animation(screen=self.screen, width=width, height=height_object,
                                       sheet_location=sheet_location, scale=scale, pixel_x=128, pixel_y=128,
                                       coordinates=(self.pos_x, self.pos_y))
        self.walk_animation = Animation(screen=self.screen, width=width, height=height_object,
                                        sheet_location=sheet_location, scale=scale, pixel_x=128, pixel_y=128,
                                        coordinates=(self.pos_x, self.pos_y))

    def mouvement(self) -> None:

        # déplace le personnage en fonction des obstacles
        oldpos = self.pos
        self.speed_x = min(20, self.speed_x)
        self.speed_y = min(20, self.speed_y)
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y
        self.pos = (self.pos_x, self.pos_y)
        self.pos_x, self.pos_y, self.speed_x, self.speed_y = bloque_sur_collision(self.level, oldpos, self.pos,
                                                                                  self.speed_x, self.speed_y)

        # teste si sous le jour il y a un du sol
        if self.speed_y == 0:
            self.can_move = True

        # anime le mouvement de course si pas dans les airs
        if self.can_move:
            if self.walk_speed <= self.speed_x < 0:
                self.walk_animation.update()
                self.walk_animation.draw(orientation='left')
            if 0 > self.speed_x <= self.walk_speed:
                self.walk_animation.update()
                self.walk_animation.draw()
        else:
            if self.speed_y > 0:
                self.jump_animation.update()
                self.jump_animation.draw()
            else:
                self.jump_animation2.update()
                self.jump_animation.draw()

        self.strength(0, 2)

    def strength(self, acceleration_x, acceleration_y) -> None:
        self.speed_x += acceleration_x
        self.speed_y += acceleration_y
        self.speed = (self.speed_x, self.speed_y)

    def show(self, surface, Screen) -> None:
        Screen.blit(surface, (self.pos_x, self.pos_y))


# _______________________________________________________________|_______________________________________________________________|_______________________________________________________________|
# _______________________________________________________________|_______________________________________________________________|_______________________________________________________________|
# _______________________________________________________________|_______________________________________________________________|_______________________________________________________________|

# Lanc
# _______________________________________________________________|

# -----------------------/
# IMPORTATION

import pygame as pg
import random
import sys

sys.path.insert(0, "Lanceur_projTransverse")

from function import parallax
from Class_Lanceur import Animation

# LANCEUR
# |
pg.init()
# |
infini = True
Lanceur = True
# |
ZoneMarquee_projetee = []
ZoneMarquee_teinte = []
# |
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
# |
ECran_afficheur = pg.display.set_mode((1900, 1000))
pg.display.set_caption("Scrolling Camera")
compte = pg.time.Clock()
# |
# |
EClargeur = 3000
SCREEN_WIDTH= 3000
EChauteur = 3000
SCREEN_HEIGHT= 3000
# |
Monde = pg.Surface((EClargeur, EChauteur))
Monde.fill(BLACK)
# |

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]

mouv_droite = False
mouv_gauche = False

# -----------------------/
# IMPORTATION_elements

# RANDOM_map

# image_E1_pA = pg.image.load("DEC\I_CORR_E1_pA.png").convert_alpha()
# image_E1_pP = pg.image.load("DEC\I_CORR_E1_pP.png").convert_alpha()

image_colE1_pA = pg.image.load("SP\Bh_E1_pA.png").convert_alpha()
image_colE1_pP = pg.image.load("SP\Bh_E1_pP.png").convert_alpha()

image_Mc_stand = pg.image.load("CP\Mc_stand.png").convert_alpha()
image_mons_des = pg.image.load("SPR\I_Monstre_desos_avantgauche.png").convert_alpha()

image_map = pg.image.load("SP\MAP.png").convert_alpha()
image_mapV6 = pg.image.load("SP\MAP_V6.png").convert_alpha()

# MONSTRE

im_monstreTest = pg.image.load("Lanceur_projTransverse/Assets/character/MOB/TestA01.png").convert_alpha()

# _______________________________________________________________|
# -----------------------/
# SEQUENCE_IM_joueur immobile_/gauche/droite
Jo_idle_g = Animation(Monde, EClargeur, EChauteur,
                      'Lanceur_projTransverse/Assets/character/player/idle_gauche.png', 1.2, 128, 128,
                      (0, 0))
Jo_idle_d = Animation(Monde, EClargeur, EChauteur,
                      'Lanceur_projTransverse/Assets/character/player/idle_droite.png', 1.2, 128, 128,
                      (0, 0))
# SEQUENCE_IM_joueur court_/gauche/droite
Jo_run_g = Animation(Monde, EClargeur, EChauteur,
                     'Lanceur_projTransverse/Assets/character/player/Run_gauche.png', 1.2, 128, 128,
                     (0, 0))
Jo_run_d = Animation(Monde, EClargeur, EChauteur,
                     'Lanceur_projTransverse/Assets/character/player/Run_droite.png', 1.2, 128, 128,
                     (0, 0))
# SEQUENCE_IM_joueur frappe1_/gauche/droite
Jo_attack_g = Animation(Monde, EClargeur, EChauteur,
                        'Lanceur_projTransverse/Assets/character/player/Attack_gauche.png', 1.2, 128, 128,
                        (0, 0))
Jo_attack_d = Animation(Monde, EClargeur, EChauteur,
                        'Lanceur_projTransverse/Assets/character/player/Attack_droite.png', 1.2, 128, 128,
                        (0, 0))
# SEQUENCE_IM_joueur frappe2_/gauche/droite
Jo_attack2_g = Animation(Monde, EClargeur, EChauteur,
                         'Lanceur_projTransverse/Assets/character/player/Attack2_gauche.png', 1.2, 128, 128,
                         (0, 0))
Jo_attack2_d = Animation(Monde, EClargeur, EChauteur,
                         'Lanceur_projTransverse/Assets/character/player/Attack2_droite.png', 1.2, 128, 128,
                         (0, 0))
# SEQUENCE_IM_joueur defense_/gauche/droite
Jo_defense_g = Animation(Monde, EClargeur, EChauteur,
                         'Lanceur_projTransverse/Assets/character/player/Defense_gauche.png', 1.2, 128, 128,
                         (0, 0))
Jo_defense_d = Animation(Monde, EClargeur, EChauteur,
                         'Lanceur_projTransverse/Assets/character/player/Defense_droite.png', 1.2, 128, 128,
                         (0, 0))
# SEQUENCE_IM_joueur defense.attaque_/gauche/droite
Jo_defatt_g = Animation(Monde, EClargeur, EChauteur,
                        'Lanceur_projTransverse/Assets/character/player/DefAttack_gauche.png', 1.2, 128, 128,
                        (0, 0))
Jo_defatt_d = Animation(Monde, EClargeur, EChauteur,
                        'Lanceur_projTransverse/Assets/character/player/DefAttack_droite.png', 1.2, 128, 128,
                        (0, 0))

# _______________________________________________________________|
# -----------------------/
# SEQUENCE_IM_Slim Idle_/gauche/droite
Mo_slim_idle_g = Animation(Monde, EClargeur, EChauteur,
                           'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_idle_gauche.png', 1.2, 128, 128,
                           (0, 0))
Mo_slim_idle_d = Animation(Monde, EClargeur, EChauteur,
                           'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_idle_droite.png', 1.2, 128, 128,
                           (0, 0))
# SEQUENCE_IM_Slim Marche_/gauche/droite
Mo_slim_marche_g = Animation(Monde, EClargeur, EChauteur,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_marche_gauche.png', 1.2, 128,
                             128,
                             (0, 0))
Mo_slim_marche_d = Animation(Monde, EClargeur, EChauteur,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_marche_droite.png', 1.2, 128,
                             128,
                             (0, 0))
# SEQUENCE_IM_Slim touche_/gauche/droite
Mo_slim_touche_g = Animation(Monde, EClargeur, EChauteur,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_touche_gauche.png', 1.2, 128,
                             128,
                             (0, 0))
Mo_slim_touche_d = Animation(Monde, EClargeur, EChauteur,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_touche_droite.png', 1.2, 128,
                             128,
                             (0, 0))
# SEQUENCE_IM_Slim mort_/1/2
Mo_slim_mort1_2 = Animation(Monde, EClargeur, EChauteur,
                            'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_mort1-2.png', 1.2, 128, 128,
                            (0, 0))
Mo_slim_mort2_2 = Animation(Monde, EClargeur, EChauteur,
                            'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_mort2-2.png', 1.2, 128, 128,
                            (0, 0))
# _______________________________________________________________|
# -----------------------/
# ENTITE_BOSS

Boss_inc = pg.image.load("Boss_LANCEUR\Boss_incant.png").convert_alpha()


# _______________________________________________________________|
# -----------------------/
# PROGRAMMATION_OBJET
# PropriétéesCiblées

# -----------------------/
# JOUEUR
class JOUEUR(pg.sprite.Sprite):
    def __init__(self, ECran_affichuer):
        pg.sprite.Sprite.__init__(self)
        self.pos_x = 0
        self.pos_y = 0
        self.pos = [self.pos_x, self.pos_y]
        self.speed_x = 0
        self.speed_y = 0
        self.speed = [self.speed_x, self.speed_y]
        self.largeur = 50
        self.hauteur = 50
        self.mass = 10

        self.max_speed = 2  # Definie la vitesse de deplacement max du joueur
        self.vie = 30000  # Definie les points de vie du joueur
        self.statut = 0
        self.portee = 130  # Definie la portee des attaques
        self.force = [50,
                      0]  # Definie les degats causes par les attaques du joueurs, et si celle-ci affligent des status
        self.size = [128, 128]
        self.scale = 1.2

        self.ecran = ECran_afficheur
        self.FrictionCoef = 0
        # Variable definissant l'action actuellement effectue par le joueur
        # [X, 0, 0, 0, 0] définie la direction du mouvement, avec 0 immobile, 1 haut, 2 bas, 3 gauche, 4 droite
        # [0, X, 0, 0, 0] définit l'intensité du mouvement, par exemple si le joueur est immobile, marche, ou court
        # [0, 0, X, 0, 0] définit l'action effectue, par exemple frapper, se guerir, interagir
        # [0, 0, 0, X, 0] sert de souvenir, en recuperant la derniere inclinaison
        # [0, 0, 0, 0, X] sert de souveni, en definissant le statut du joueur relatif au combat, ici 0 neutre, 1 invulnerable due a des dommages subis, 2 invulnerable due a des facteurs exterieurs
        self.action = [0, 0, 0, 0, 0]
        self.rect = pg.Rect (self.pos_x,  self.pos_y, self.size[0], self.size[1])
        self.currentLevel = None

    def regard_statut(self, zonemarquee):

        vie_originale = self.vie

        # Dans le cas où le joueur se retrouve au sein d'une zone marquee, on applique les instructions donnees par la zone
        for x in range(len(zonemarquee)):
            if self.pos_x > zonemarquee[x][0] and self.pos_x <= zonemarquee[x][2] and self.pos_y > zonemarquee[x][
                1] and self.pos_y <= zonemarquee[x][3] and self.action[4] == 0:
                # Si definie, inflige/octroie des points de vie
                self.vie -= zonemarquee[x][4][0]
                if self.vie < vie_originale:
                    self.action[1] == 1
            elif self.vie <= 0:
                self.action[1] == 1
                infini = False
                return infini

            self.statut = zonemarquee[x][4][1]  # Si definie, herite un statut au joueur

    def mouvement_action(self, pos_cam):

        pos_x = pos_cam[0]
        pos_y = pos_cam[1]

        # Recup l'input clavier
        ClavIn = pg.key.get_pressed()

        # MOUVEMENT_joueur

        # Mouvement_AVANT
        # En plus de regarder si le joueur presse "UP", on s'assure que celui n'effectue pas l'action "RUEE"
        # L'action concernee ne pouvant avoir en lieu en meme temps
        if ClavIn[pg.K_UP] and ClavIn[pg.K_KP4] == False:
            self.speed_y -= self.max_speed
            pos_y += self.max_speed
            self.action[0] = 1

        # Mouvement_ARRIERE
        if ClavIn[pg.K_DOWN] and ClavIn[pg.K_KP4] == False:
            self.speed_y += self.max_speed  # Deplacement_joueur
            pos_y -= self.max_speed  # Deplacement_camera
            self.action[0] = 2  # Action_joueur (Soit ici, se deplacer vers le bas)

        # Mouvement_GAUCHE
        if ClavIn[pg.K_LEFT] and ClavIn[pg.K_KP4] == False:
            self.speed_x -= self.max_speed
            pos_x += self.max_speed
            self.action[0] = 3
            self.action[3] = 1

        # Mouvement_DROITE
        if ClavIn[pg.K_RIGHT] and ClavIn[pg.K_KP4] == False:
            self.speed_x += self.max_speed
            pos_x -= self.max_speed
            self.action[0] = 4
            self.action[3] = 0

        # CONTROLE_SortieDeMap

        # LIMITE_frontiere (Elements interieurs exclus)
        lim_supx = EClargeur - self.largeur * 2
        lim_infx = 0 - self.largeur
        lim_supy = EChauteur - self.hauteur * 3
        lim_infy = 0 - self.hauteur * 1.5

        if self.pos_x < lim_infx:
            self.pos_x = lim_infx
            pos_x = pos_cam[0]
        elif self.pos_x > lim_supx:
            self.pos_x = lim_supx
            pos_x = pos_cam[0]

        if self.pos_y < lim_infy:
            self.pos_y = lim_infy
            pos_y = pos_cam[1]
        elif self.pos_y > lim_supy:
            self.pos_y = lim_supy
            pos_y = pos_cam[1]

        # ACTION_joueur
        # ACT_ATTAQUE
        if ClavIn[pg.K_KP0]:
            # ATTAQUER
            self.action[2] = 1
            zm_g = [self.pos_x - self.portee - 5, self.pos_y - self.portee - 5, self.pos_x - 5, self.pos_y + 50,
                    self.force]
            zm_d = [self.pos_x + 5, self.pos_y - 50, self.pos_x + self.portee + 5, self.pos_y + self.portee + 5,
                    self.force]
            # On determine le sens de l'attaque, pour definir correctement la zone marquee
            if self.action[3] == 1:  # GAUCHE
                print("Gauche", zm_g)
                Debut(zm_g)
            else:  # DROITE
                print("Droite", zm_d)
                Debut(zm_d)

        # ACT_DEFENSE
        if ClavIn[pg.K_KP1]:
            # SE DEFENDRE
            self.action[2] = 2
        # ACT_RUEE
        if ClavIn[pg.K_LEFT] and ClavIn[pg.K_KP4]:
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

        # POSSIBILITE_joueur
        # En pressant la touche "a", le joueur met fin au programme

        if ClavIn[pg.K_a]:
            infini = False
            return infini

        return (pos_x, pos_y)

    # Affiche le sprite du joueur, en prenant en compte le mouvement effectue

    def update(self):
        self.rect.x += self.speed_x
        tileHitList = pg.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        #Move player to correct side of that block
        for tile in tileHitList:
            if self.speed_x > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
        difference_y, difference = 0, 0
        # Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - SCREEN_WIDTH//10:
            difference = -(self.rect.right - (SCREEN_WIDTH //10))
            self.rect.right = SCREEN_WIDTH - SCREEN_WIDTH //10

        if self.rect.left <= SCREEN_WIDTH//10:
            difference = SCREEN_WIDTH//10 - self.rect.left
            self.rect.left = SCREEN_WIDTH//10

        if self.rect.bottom >= SCREEN_HEIGHT - SCREEN_WIDTH//40:
            difference_y = -(self.rect.bottom - (SCREEN_HEIGHT - SCREEN_WIDTH//40))
            self.rect.bottom = SCREEN_HEIGHT - (SCREEN_WIDTH//40)

        if self.rect.top <= SCREEN_WIDTH//20:
            difference_y = SCREEN_WIDTH//20 - self.rect.top
            self.rect.top = SCREEN_WIDTH//20
        self.currentLevel.shiftLevel(difference, difference_y)

        self.rect.y += self.speed_y #Update player position

        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)

        if len(tileHitList) > 0:
            for tile in tileHitList:
                if self.speed_y > 0:
                    self.rect.bottom = tile.rect.top
                    self.speed_y = 1
                    #TODO: refait les annimation
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
            """"
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

    def rendu(self, Afficheur):

        # Dessine une barre de vie
        pg.draw.rect(ECran_afficheur, (255, 0, 0), (50, 100, 70, 35))
        pg.draw.rect(ECran_afficheur, (0, 128, 0), (50, 100, 20 - (5 * (10 - self.vie // 400)), 35))

        # Action_AVANT
        if self.action[0] == 1:
            Jo_run_d.draw((self.pos_x, self.pos_y))
            Jo_run_d.update()
            self.action[0] = 0

        # Action_ARRIERE
        elif self.action[0] == 2:
            Jo_run_g.draw((self.pos_x, self.pos_y))
            Jo_run_g.update()
            self.action[0] = 0

        # Action_GAUCHE
        elif self.action[0] == 3:
            if self.action[2] == 1:
                Jo_defatt_g.draw((self.pos_x, self.pos_y))
                Jo_defatt_g.update()
                self.action[0] = 0
                self.action[2] = 0
            # elif self.action[2] == 3: EN ATTENTE, manque animation "dash", soit celle de la ruee

            else:
                Jo_run_g.draw((self.pos_x, self.pos_y))
                Jo_run_g.update()
                self.action[0] = 0

        # Action_DROITE
        elif self.action[0] == 4:
            if self.action[2] == 1:
                Jo_defatt_d.draw((self.pos_x, self.pos_y))
                Jo_defatt_d.update()
                self.action[0] = 0
                self.action[2] = 0
            else:
                Jo_run_d.draw((self.pos_x, self.pos_y))
                Jo_run_d.update()
                self.action[0] = 0

        # Action_IMMOBILE
        else:
            if self.action[2] == 1:  # ATTAQUE
                if self.action[3] == 1:
                    Jo_attack_g.draw((self.pos_x, self.pos_y))
                    Jo_attack_g.update()
                    self.action[2] = 0
                else:
                    Jo_attack_d.draw((self.pos_x, self.pos_y))
                    Jo_attack_d.update()
                    self.action[2] = 0

            elif self.action[2] == 2:  # DEFENSE
                if self.action[3] == 1:
                    Jo_defense_g.draw((self.pos_x, self.pos_y))
                    Jo_defense_g.update()
                    self.action[2] = 0
                else:
                    Jo_defense_d.draw((self.pos_x, self.pos_y))
                    Jo_defense_d.update()
                    self.action[2] = 0

            else:
                if self.action[3] == 1:
                    Jo_idle_g.draw((self.pos_x, self.pos_y))
                    Jo_idle_g.update()
                else:
                    Jo_idle_d.draw((self.pos_x, self.pos_y))
                    Jo_idle_d.update()
        if self.speed > 2:
            self.speed -= 1

            # Afficheur.blit(image_Mc_stand, (self.pos_x, self.pos_y)) #/!\ version statique


# -----------------------/
# MONSTRES

class MONSTRE:
    def __init__(self, pos_x, pos_y, largeur, hauteur, mass, vitesse, scale, ecran, friction_coef, campeur, attention,
                 etat, vie) -> None:
        # |
        # Ensemble de variable définissant la position du monstre dans l'espace "Monde"
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = [self.pos_x, self.pos_y]
        # |
        # Definie les proportions/caracteristiques physique du monstre
        self.largeur = largeur
        self.hauteur = hauteur
        self.mass = mass
        # |
        # Definie la vitesse de deplacement actuelle du monstre
        self.speed = vitesse
        # Definie les points de vie du monstre
        self.vie = vie
        # |
        # Definie les parametres relatifs au rendue de l'image du monstre
        self.scale = scale
        self.ecran = ecran
        self.FrictionCoef = friction_coef
        # |
        self.force = 50
        # |
        # Definie un espace où le monstre trouvera sa position initial, ainsi que sa zone de patrouille
        self.campeur = campeur
        # Définie l'attention du montre, soit plus haute est la valeur plus loin le monstre peut voir le joueur
        self.attention = attention
        # Definie l'etat actuel du monstre, soit passif, en fuite, en chasse...
        self.etat = etat
        # |
        # [X, 0, 0, 0]Definie le sens dans laquelle se deplace l'ennemi, ici 0 immobile, 1 gauche et 2 droite
        # [0, 0, 0, X]Sert de souvenir, rappelle la derniere inclinaison (0 gauche ou 1 droite)
        self.action = [0, 0, 0, 0, 0]
        # |

    # -----------------------/

    def regard_statut(self, zonemarquee):

        vie_originale = self.vie

        for x in range(len(zonemarquee)):
            print("CHECK", zonemarquee, (self.pos_x, self.pos_y))
            # Dans le cas où le monstre se retrouve au sein d'une zone marquee, on applique les instructions donnees par la zone
            if self.pos_x > zonemarquee[x][0] and self.pos_x <= zonemarquee[x][2] and self.pos_y > zonemarquee[x][
                1] and self.pos_y <= zonemarquee[x][3] and self.action[4] == 0:
                # Si definie, inflige/octroie des points de vie
                self.vie -= zonemarquee[x][4][0]

                if self.vie < vie_originale:
                    print("Attention", self.vie)
                    self.action[4] = 1
                    self.etat = 0
                    if self.vie <= 0:
                        self.action[4] = 9
                        # Dans le cas où le monstre est mort, on supprime l'instance qui lui est associee

                    # Si definie, cause un statut au monstre
                    self.statut = zonemarquee[x][4][1]

    # -----------------------/

    def PatrouilleRecherche(self, Position_joueur):
        # Fonction definissant les actions a effectues aux monstres
        # Regarde si le joueur se retrouve dans la zone d'attention du monstre, et si telle est le cas, change l'etat du monstre en mode chasse
        if self.attention >= abs(self.pos_x) - Position_joueur[0] and self.attention >= abs(self.pos_y) - \
                Position_joueur[0] and self.action[4] != 9:
            self.etat = 1

        # Uniquement en mode chasse, le monstre poursuivra le joueur
        if self.etat == 1 and self.action[4] != 1 and Position_joueur != self.pos:
            if self.pos_x < Position_joueur[0] - self.largeur:
                self.pos_x += self.speed
                self.action[0] = 2
            elif self.pos_x > Position_joueur[0] + self.largeur:
                self.pos_x -= self.speed
                self.action[0] = 1

            if self.pos_y < Position_joueur[1]:
                self.pos_y += self.speed

            elif self.pos_y > Position_joueur[1]:
                self.pos_y -= self.speed

        else:
            self.etat == 0


    def rendu(self, Afficheur):
        print(self.action)

        # Dessine une barre de vie
        if self.etat != -4:
            pg.draw.rect(Monde, (255, 0, 0), (self.pos_x + 40, self.pos_y + 100, 70, 5))
            pg.draw.rect(Monde, (0, 128, 0), (self.pos_x + 40, self.pos_y + 100, 20 - (5 * (10 - self.vie // 400)), 5))

        if self.action[4] == 9:  # MORT
            if self.etat == -4:
                Mo_slim_mort2_2.draw((self.pos_x, self.pos_y))
            else:
                Mo_slim_mort1_2.draw((self.pos_x, self.pos_y))
                Mo_slim_mort1_2.update()
                self.etat -= 1

        elif self.action[4] == 1:  # SUBIT DES COUPS
            if self.action[3] == 0:
                Mo_slim_touche_g.draw((self.pos_x, self.pos_y))
                Mo_slim_touche_g.update()
                self.action[4] = 0
            else:
                Mo_slim_touche_d.draw((self.pos_x, self.pos_y))
                Mo_slim_touche_d.update()
                self.action[4] = 0

        elif self.action[0] == 1:  # DEPLACEMENT_GAUCHE
            Mo_slim_marche_g.draw((self.pos_x, self.pos_y))
            Mo_slim_marche_g.update()

        elif self.action[0] == 2:  # DEPLACEMENT_DROITE
            Mo_slim_marche_d.draw((self.pos_x, self.pos_y))
            Mo_slim_marche_d.update()

        else:  # IMMOBILE
            if self.action[3] == 0:
                Mo_slim_idle_g.draw((self.pos_x, self.pos_y))
                Mo_slim_idle_g.update()
            else:
                Mo_slim_idle_d.draw((self.pos_x, self.pos_y))
                Mo_slim_idle_d.update()


# -----------------------/
class ZONE_MARQUEE:
    def __init__(self, pos_1_x, pos_1_y, pos_2_x, pos_2_y, force):
        self.pos_1_x = pos_1_x  # ^ Y
        self.pos_1_y = pos_1_y  # |
        self.pos_2_x = pos_2_x  # |
        self.pos_2_y = pos_2_y  # (x,y) |---------------> X   [x, y, X, Y, causalité(degat/soint, statut)] organisation de "zonemarquee"
        # |
        # Relai a "force"
        self.force = force
        # |
        self.archive = []


def Debut(zm):
    ZoneMarquee_monde1.archive.append(zm)


def Fin():
    ZoneMarquee_monde1.archive = ZoneMarquee_monde1.archive.pop(0)


# _______________________________________________________________|
# -----------------------/
# FONCTIONS
# -----------------------/


# -----------------------/
# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
# CREATION_ZoneMarquee_relatif_monde1
ZoneMarquee_monde1 = ZONE_MARQUEE(9999, 9999, 9999, 9999, [9999, 9999])


# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
# -----------------------/
def MAIN_appelINFINI(Afficheur, compte):
    # |

    # |
    for x in range(10):
        pg.draw.rect(Monde, BLUE, ((x * 100, x * 100), (20, 20)))

    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
    # CREATION_Joueur
    Jo = JOUEUR()
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
    # |
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
    # CREATION_Monstre
    # |
    Mo_slim1 = MONSTRE(1000, 300, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    Mo_slim2 = MONSTRE(1500, 50, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    Mo_slim3 = MONSTRE(2000, 200, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    Mo_slim4 = MONSTRE(1700, 250, 50, 50, 0, 1, 3, ECran_afficheur, 0, (0, 0), 500, 0, 8000)
    list_slim = [Mo_slim1, Mo_slim2, Mo_slim3, Mo_slim4]
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
    pos_cam = [500, 500]
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
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
        pos_cam = Jo.mouvement_action(pos_cam)
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
        Monde.fill(BLACK)
        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
        # RENDU_MAP
        Monde.blit(image_mapV6, (0, 0))  # image_colE1_pP
        # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
        # |
        for x in range(10):
            pg.draw.rect(Monde, BLUE, ((x * 100, x * 100), (20, 20)))

        # --|
        # RENDU_Monstre
        # RENDU_BOSS
        Monde.blit(Boss_inc, (1300, 850))
        # RENDU_Monstre
        # Monde.blit(im_monstreTest, (Mo.pos_x, Mo.pos_y))

        for Slim in list_slim:
            Slim.rendu(Monde)

        # -|
        # RENDU_Joueur
        Jo.rendu(Monde)

        # -|
        # RENDU_FONDMonde
        ECran_afficheur.blit(Monde, pos_cam)
        # --|
        # Monde.blit(image_colE1_pA, (0, 200))

        # |

        # |

        pg.display.flip()


# PROPAGATEUR_lineaire
if Lanceur:
    # |

    # |
    MAIN_appelINFINI(ECran_afficheur, compte)
