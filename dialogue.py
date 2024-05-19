import pygame


class Dialogue:
    def __init__(self, screen, height, width, box_width, box_height, x, y, text, color):

        from Class import Animation
        self.text_surfaces = []  # on stocke les surfaces de texte pour les afficher sans animation
        self.screen = screen
        self.width = width
        self.height = height
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.Font('Assets/font/Pixeled.ttf', 15)
        self.rect = pygame.Rect(x, y, box_width, box_height)
        self.counter = 0
        self.speed = 1
        self.active_dialogue = 0
        self.lines = text
        self.text = text[self.active_dialogue]
        self.done = False
        self.run = True

        for lines in self.lines:
            self.text_surfaces.append(self.font.render(lines, True, self.color))
            # on génère une surface pour chaque ligne de texte pour les afficher plus tard sans animation

        self.space_button = Animation(screen, width, height, 'Assets/menu/space_button/space_button_spritesheet.png', 2,
                                      64, 16,
                                      (x + box_width - 175, y + box_height - 50))

    def draw(self):
        if self.run:
            self.counter += self.speed
            text_surface = self.font.render(self.text[:self.counter], True, self.color)
            pygame.draw.rect(self.screen, (0, 0, 0), self.rect)
            self.screen.blit(text_surface, (self.x + 20, self.y + 10 + 40 * self.active_dialogue))
            # on affiche le texte avec une animation de défilement

            for i in range(len(self.lines)):
                if i < self.active_dialogue:
                    self.screen.blit(self.text_surfaces[i], (self.x + 20, self.y + 10 + 40 * i))
                    # on affiche les lignes de texte déjà affichées sans animation

            if self.counter < len(self.text):
                self.counter += 1

                # on fait défiler le texte

            elif self.counter >= len(self.text):
                self.done = True
                self.space_button.draw()
                self.space_button.update()

                # on indique que l'animation est terminée
            self.text = self.lines[self.active_dialogue]
            # on récupère la ligne de texte correspondant à l'indice actif car le texte est slice par chaque caractère

    def skip(self):
        self.counter += 4
        if self.counter >= len(self.text):
            self.counter = len(self.text)
        # on fait défiler le texte plus rapidement si le joueur appuie sur la touche espace

    def next(self):

        if self.done and self.active_dialogue < len(self.lines) - 1:
            self.text = self.text[self.active_dialogue]
            self.active_dialogue += 1
            self.done = False
            self.counter = 0
        # on passe à la ligne de texte suivante si l'animation est terminée et qu'il reste des lignes de texte

    def closed(self):
        if self.active_dialogue == len(self.lines) - 1 and self.done:
            self.run = False
            return True
    # on arrête l'animation si toutes les lignes de texte ont été affichées
