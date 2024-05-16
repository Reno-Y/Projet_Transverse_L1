import pygame as pg
from Class import Animation


SCREEN_WIDTH, SCREEN_HEIGHT = pg.display.Info().current_w, pg.display.Info().current_h
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

Mo_slim_idle_g = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                           'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_idle_gauche.png', 1.2, 128, 128,
                           (0, 0))
Mo_slim_idle_d = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                           'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_idle_droite.png', 1.2, 128, 128,
                           (0, 0))
# SEQUENCE_IM_Slim Marche_/gauche/droite
Mo_slim_marche_g = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_marche_gauche.png', 1.2, 128,
                             128,
                             (0, 0))
Mo_slim_marche_d = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_marche_droite.png', 1.2, 128,
                             128,
                             (0, 0))
# SEQUENCE_IM_Slim touche_/gauche/droite
Mo_slim_touche_g = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_touche_gauche.png', 1.2, 128,
                             128,
                             (0, 0))
Mo_slim_touche_d = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                             'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_touche_droite.png', 1.2, 128,
                             128,
                             (0, 0))
# SEQUENCE_IM_Slim mort_/1/2
Mo_slim_mort1_2 = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                            'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_mort1-2.png', 1.2, 128, 128,
                            (0, 0))
Mo_slim_mort2_2 = Animation(screen, SCREEN_WIDTH, SCREEN_HEIGHT,
                            'Lanceur_projTransverse/Assets/character/MOB/Mob_Slim/Slim_mort2-2.png', 1.2, 128, 128,
                            (0, 0))

class MONSTRE:
    def __init__(self, pos_x, pos_y, width_hitbox, height_hitbox, mass, speed, scale, screen, friction_coef,
                 state, life):

        # Ensemble de variable définissant la position du monstre dans l'espace "Monde"
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos = [self.pos_x, self.pos_y]

        # Definie les proportions/caracteristiques physique du monstre
        self.hitbox_width = width_hitbox
        self.hitbox_height = height_hitbox
        self.mass = mass

        # Definie la vitesse de deplacement actuelle du monstre
        self.speed = speed
        # Definie les points de vie du monstre
        self.life = life

        # Definie les parametres relatifs au rendue de l'image du monstre
        self.scale = scale
        self.ecran = screen
        self.FrictionCoef = friction_coef

        self.force = 50

        # Definie l'etat actuel du monstre, soit passif, en fuite, en chasse...
        self.state = state

        # [X, 0, 0, 0]Definie le sens dans laquelle se deplace l'ennemi, ici 0 immobile, 1 gauche et 2 droite
        # [0, 0, 0, X]Sert de souvenir, rappelle la derniere inclinaison (0 gauche ou 1 droite)
        self.action = [0, 0, 0, 0, 0]


    def check_state(self, marked_zone):

        life = self.life

        for x in range(len(marked_zone)):

            # Dans le cas où le monstre se retrouve au sein d'une zone marquee, on applique les instructions donnees par la zone

            if self.pos_x > marked_zone[x][0] and self.pos_x <= marked_zone[x][2] and self.pos_y > marked_zone[x][
                1] and self.pos_y <= marked_zone[x][3] and self.action[4] == 0:

                # Si definie, inflige/octroie des points de vie
                self.life -= marked_zone[x][4][0]

                if self.life < life:
                    self.action[4] = 1
                    self.state = 0
                    if self.life <= 0:
                        self.action[4] = 9
                        # Dans le cas où le monstre est mort, on supprime l'instance qui lui est associee

                    # Si definie, cause un statut au monstre
                    self.statut = marked_zone[x][4][1]

    # -----------------------/

    def patrol_search(self, Position_joueur):
        # Fonction definissant les actions a effectues aux monstres
        # Regarde si le joueur se retrouve dans la zone d'attention du monstre, et si telle est le cas, change l'etat du monstre en mode chasse
        if 500 >= abs(self.pos_x) - Position_joueur[0] and 500 >= abs(self.pos_y) - \
                Position_joueur[0] and self.action[4] != 9:
            self.state = 1

        # Uniquement en mode chasse, le monstre poursuivra le joueur
        if self.state == 1 and self.action[4] != 1 and Position_joueur != self.pos:
            if self.pos_x < Position_joueur[0] - self.hitbox_width:
                self.pos_x += self.speed
                self.action[0] = 2
            elif self.pos_x > Position_joueur[0] + self.hitbox_width:
                self.pos_x -= self.speed
                self.action[0] = 1

            if self.pos_y < Position_joueur[1]:
                self.pos_y += self.speed

            elif self.pos_y > Position_joueur[1]:
                self.pos_y -= self.speed

        else:
            self.state == 0

    def draw(self):

        # Dessine une barre de vie
        if self.state != -4:
            pg.draw.rect(screen, (255, 0, 0), (self.pos_x + 40, self.pos_y + 100, 70, 5))
            pg.draw.rect(screen, (0, 128, 0),
                         (self.pos_x + 40, self.pos_y + 100, 20 - (5 * (10 - self.life // 400)), 5))

        if self.action[4] == 9:  # MORT
            if self.state == -4:
                Mo_slim_mort2_2.draw((self.pos_x, self.pos_y))
            else:
                Mo_slim_mort1_2.draw((self.pos_x, self.pos_y))
                Mo_slim_mort1_2.update()
                self.state -= 1

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
