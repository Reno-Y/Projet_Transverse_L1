#Lanc
#_______________________________________________________________|

#-----------------------/
#IMPORTATION

import pygame as pg
import random
import sys

sys.path.insert(0, "Lanceur_projTransverse")

from function import parallax
from Class import Animation


#LANCEUR
pg.init()
infini = True
Lanceur = True

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
#|
ECran_afficheur = pg.display.set_mode((2000, 1000))
pg.display.set_caption("Scrolling Camera")
compte = pg.time.Clock()
#|
#|
EClargeur = 3000
EChauteur = 3000
#|
Monde = pg.Surface((EClargeur, EChauteur))
Monde.fill(BLACK)
#|
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]

mouv_droite = False
mouv_gauche = False

#-----------------------/
#IMPORTATION_elements

image_E1_pA = pg.image.load("DEC\I_CORR_E1_pA.png").convert_alpha()
image_E1_pP = pg.image.load("DEC\I_CORR_E1_pP.png").convert_alpha()

image_colE1_pA = pg.image.load("SP\Bh_E1_pA.png").convert_alpha()
image_colE1_pP = pg.image.load("SP\Bh_E1_pP.png").convert_alpha()


image_Mc_stand = pg.image.load("CP\Mc_stand.png").convert_alpha()
image_mons_des = pg.image.load("SPR\I_Monstre_desos_avantgauche.png").convert_alpha()
image_map = pg.image.load("SP\MAP.png").convert_alpha()
image_mapV2 = pg.image.load("SP\MAP_V2.jpg").convert_alpha()


#SEQUENCE_IM_joueur immobile_/gauche/droite
Jo_idle_g = Animation(Monde, EClargeur, EChauteur,
                                'Lanceur_projTransverse/Assets/character/player/idle_gauche.png', 1.2, 128, 128,
                                (0, 0))
Jo_idle_d = Animation(Monde, EClargeur, EChauteur,
                                'Lanceur_projTransverse/Assets/character/player/idle_droite.png', 1.2, 128, 128,
                                (0, 0))
#SEQUENCE_IM_joueur court_/gauche/droite
Jo_run_g = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Run_gauche.png', 1.2, 128, 128,
                               (0, 0))
Jo_run_d = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Run_droite.png', 1.2, 128, 128,
                               (0, 0))
#SEQUENCE_IM_joueur frappe1_/gauche/droite
Jo_attack_g = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Attack_gauche.png', 1.2, 128, 128,
                               (0, 0))
Jo_attack_d = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Attack_droite.png', 1.2, 128, 128,
                               (0, 0))
#SEQUENCE_IM_joueur frappe2_/gauche/droite
Jo_attack2_g = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Attack2_gauche.png', 1.2, 128, 128,
                               (0, 0))
Jo_attack2_d = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Attack2_droite.png', 1.2, 128, 128,
                               (0, 0))
#SEQUENCE_IM_joueur defense_/gauche/droite
Jo_defense_g = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Defense_gauche.png', 1.2, 128, 128,
                               (0, 0))
Jo_defense_d = Animation(Monde, EClargeur, EChauteur,
                               'Lanceur_projTransverse/Assets/character/player/Defense_droite.png', 1.2, 128, 128,
                               (0, 0))


#_______________________________________________________________|
#-----------------------/
#PROGRAMMATION_OBJET
#PropriétéesCiblées

#-----------------------/
#JOUEUR
class JOUEUR:
    def __init__(self, pos_x, pos_y, largeur, hauteur, mass, speed, scale, ecran, friction_coef) -> None:
        #|
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = [self.pos_x, self.pos_y]
        #|
        self.largeur = largeur
        self.hauteur = hauteur
        self.mass = mass
        #|
        self.speed = speed
        #|
        self.scale = scale
        self.ecran = ecran
        self.FrictionCoef = friction_coef
        #|
        #Variable definissant l'action actuellement effectue par le joueur
        #[X, 0, 0, 0] définie la direction du mouvement, avec 0 immobile, 1 haut, 2 bas, 3 gauche et 4 droite
        #[0, X, 0, 0] définit l'intensité du mouvement, par exemple si le joueur est immobile, marche, ou court
        #[0, 0, X, 0] définit l'action effectue, par exemple frapper, se guerir, interagir
        #[0, 0, 0, X] sert de souvenir, en recuperant la derniere inclinaison
        self.action = [0, 0, 0, 0]
        #|

    # -----------------------/
    def mouvement_action(self, pos_cam):

        #self.action = [0, 0, 0]



        pos_x = pos_cam[0]
        pos_y = pos_cam[1]

        #Recup l'input clavier
        ClavIn = pg.key.get_pressed()

        #MOUVEMENT_joueur

        #Mouvement_AVANT
        if ClavIn[pg.K_UP]:
            self.pos_y -= self.speed
            pos_y += self.speed
            self.action[0] = 1

        #Mouvement_ARRIERE
        if ClavIn[pg.K_DOWN]:
            #Deplacement_joueur
            self.pos_y += self.speed
            #Deplacement_camera
            pos_y -= self.speed
            #Action_joueur (Soit ici, se deplacer vers le bas)
            self.action[0] = 2

        #Mouvement_GAUCHE
        if ClavIn[pg.K_LEFT]:
            self.pos_x -= self.speed
            pos_x += self.speed
            self.action[0] = 3
            self.action[3] = 1

        #Mouvement_DROITE
        if ClavIn[pg.K_RIGHT]:
            self.pos_x += self.speed
            pos_x -= self.speed
            self.action[0] = 4
            self.action[3] = 0

        #CONTROLE_SortieDeMap

        #LIMITE_frontiere (Elements interieurs exclus)
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
        if ClavIn[pg.K_KP0]:
            #ATTAQUER
            self.action[2] = 1

        if ClavIn[pg.K_KP1]:
            #SE DEFENDRE
            self.action[2] = 2

        # POSSIBILITE_joueur
        # En pressant la touche "a", le joueur met fin au programme

        if ClavIn[pg.K_a]:
            infini = False
            return infini

        return (pos_x, pos_y)

    #Affiche le sprite du joueur, en prenant en compte le mouvement effectue
    def rendu(self, Afficheur):

        #Action_AVANT
        if self.action[0] == 1:
            Jo_run_d.draw((self.pos_x, self.pos_y))
            Jo_run_d.update()
            self.action[0] = 0

        #Action_ARRIERE
        elif self.action[0] == 2:
            Jo_run_g.draw((self.pos_x, self.pos_y))
            Jo_run_g.update()
            self.action[0] = 0

        #Action_GAUCHE
        elif self.action[0] == 3:
            Jo_run_g.draw((self.pos_x, self.pos_y))
            Jo_run_g.update()
            self.action[0] = 0

        #Action_DROITE
        elif self.action[0] == 4:
            Jo_run_d.draw((self.pos_x, self.pos_y))
            Jo_run_d.update()
            self.action[0] = 0


        #Action_IMMOBILE
        else:
            if self.action[2] == 1: #ATTAQUE
                if self.action[3] == 1:
                    Jo_attack_g.draw((self.pos_x, self.pos_y))
                    Jo_attack_g.update()
                    self.action[2] = 0
                else:
                    Jo_attack_d.draw((self.pos_x, self.pos_y))
                    Jo_attack_d.update()
                    self.action[2] = 0

            elif self.action[2] == 2: #DEFENSE
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

            #Afficheur.blit(image_Mc_stand, (self.pos_x, self.pos_y)) #/!\ version statique


#_______________________________________________________________|
#-----------------------/
#FONCTIONS

def MAIN_appelINFINI(Afficheur, compte):
    for x in range(10):
        pg.draw.rect(Monde,BLUE,((x*100,x*100),(20,20)))

    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
    Jo = JOUEUR(0, 0, 50, 50, 0, 2, 4, ECran_afficheur, 0)
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]
    pos_cam = [500, 500]
    # |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]

    while infini:
        compte.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return None
        #|
        pos_cam = Jo.mouvement_action(pos_cam)
        #|
        ECran_afficheur.fill(WHITE)
        #|
        Monde.fill(BLACK)
        Monde.blit(image_colE1_pP, (0, 0))
        #|
        for x in range(10):
            pg.draw.rect(Monde,BLUE,((x*100,x*100),(20,20)))
        #--|
        Jo.rendu(Monde)
        ECran_afficheur.blit(Monde, pos_cam)
        #--|
        Monde.blit(image_colE1_pA, (0, 200))

        pg.display.flip()

#PROPAGATEUR_lineaire
if Lanceur:

    MAIN_appelINFINI(ECran_afficheur, compte)






