import math
import pygame


class Entity:
    def __init__(self, pos, size, assets, type):
        self.pos = list(pos).copy()
        self.speed = [0.0, 0.0]
        self.size = list(size).copy()
        self.mass = 10
        self.assets = assets
        self.type = type
        self.flipped = [False, True]
        self.centered = False
        self.angle = 0
        self.opacity = 255
        self.scale = [1, 1]
        self.actual_animation = None
        self.show = False

    @property
    def hit_box(self):
        """permet de crée la hit box"""
        if self.centered:
            return pygame.Rect((self.pos[0] - (self.size[0] // 2)) // 1, (self.pos[1] - (self.size[1] // 2)) // 1,
                               self.size[0], self.size[1])
        else:
            return pygame.Rect(self.pos[0] // 1, self.pos[1] // 1, self.size[0], self.size[1])

    @property
    def center(self):
        """permet de centrer la position"""
        if self.centered:
            return self.pos.copy()
        else:
            self.pos = [self.pos[0] + (self.size[0] // 2), self.pos[1] + (self.size[1] // 2)]
            return self.pos.copy()

    def get_distance(self, target):
        try:
            # distance d'une entité
            return math.sqrt((target.pos[0] - self.pos[0]) ** 2 + (target.pos[1] - self.pos[1]) ** 2)
        except:
            # distance d'une position
            return math.sqrt((target[0] - self.pos[0]) ** 2 + (target[1] - self.pos[1]) ** 2)

    def in_range(self, target, range_):
        return self.get_distance(target) <= range_

    def animation_select(self):
        # TODO: faire les animation en fonction du déplacment
        pass

    def collision(self, rects):
        old_rect = self.hit_box
        new_rect = old_rect.copy()
        new_rect.topleft = (old_rect.x + self.speed[0], old_rect.y + self.speed[0])
        collide_later = []
        for block in rects:
            if not new_rect.colliderect(block):
                continue

            dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
            # Dans cette première phase, on n'ajuste que les pénétrations sur un seul axe.
            if dx_correction == 0.0:
                new_rect.top += dy_correction
                self.speed[1] = 0.0
            elif dy_correction == 0.0:
                new_rect.left += dx_correction
                self.speed[0] = 0.0
            else:
                collide_later.append(block)

        # Deuxième phase. On teste à présent les distances de pénétrations pour
        # les blocks qui en possédaient sur les 2 axes.
        for block in collide_later:
            dx_correction, dy_correction = compute_penetration(block, old_rect, new_rect)
            if dx_correction == dy_correction == 0.0:
                # Finalement plus de pénétration. Le new_rect a bougé précédemment
                # lors d'une résolution de collision
                continue
            if abs(dx_correction) < abs(dy_correction):
                # Faire la correction que sur l'axe X (plus bas)
                dy_correction = 0.0
            elif abs(dy_correction) < abs(dx_correction):
                # Faire la correction que sur l'axe Y (plus bas)
                dx_correction = 0.0
            if dy_correction != 0.0:
                new_rect.top += dy_correction
                self.speed[1] = 0.0
            elif dx_correction != 0.0:
                new_rect.left += dx_correction
                self.speed[0] = 0.0
        self.pos = new_rect.topleft

    def move(self, rects):
        self.speed[0] = min(20., self.speed[0])
        self.speed[1] = min(20., self.speed[1])
        self.collision(rects)
        self.animation_select()


def compute_penetration(block, old_rect, new_rect):
    dx_correction = dy_correction = 0.0
    if old_rect.bottom <= block.top < new_rect.bottom:
        dy_correction = block.top - new_rect.bottom
    elif old_rect.top >= block.bottom > new_rect.top:
        dy_correction = block.bottom - new_rect.top
    if old_rect.right <= block.left < new_rect.right:
        dx_correction = block.left - new_rect.right
    elif old_rect.left >= block.right > new_rect.left:
        dx_correction = block.right - new_rect.left
    return dx_correction, dy_correction
