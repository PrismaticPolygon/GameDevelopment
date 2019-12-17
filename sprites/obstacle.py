import pygame as pg
from settings import WALL_LAYER


def collide_with_walls(sprite, group, dir):

    if dir == 'sprites':

        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

        if hits:

            if hits[0].rect.centerx > sprite.hit_rect.centerx: # Sprite moving right

                sprite.position.x = hits[0].rect.left - sprite.hit_rect.width / 2

            if hits[0].rect.centerx < sprite.hit_rect.centerx:

                sprite.position.x = hits[0].rect.right + sprite.hit_rect.width / 2

            sprite.velocity.x = 0
            sprite.hit_rect.centerx = sprite.position.x

    if dir == 'y':

        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

        if hits:

            if hits[0].rect.centery > sprite.hit_rect.centery:  # Sprite moving down

                sprite.position.y = hits[0].rect.top - sprite.hit_rect.height / 2

            if hits[0].rect.centery < sprite.hit_rect.centery:

                sprite.position.y = hits[0].rect.bottom + sprite.hit_rect.height / 2

            sprite.velocity.y = 0
            sprite.hit_rect.centery = sprite.position.y

def collide_hit_rect(one, two):

    return one.hit_rect.colliderect(two.rect)

class Obstacle(pg.sprite.Sprite):

    def __init__(self, game, x, y, width, height):

        # Game variables

        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Object variables

        self.rect = pg.Rect(x, y, width, height)
        self.hit_rect = self.rect

        self.x = x
        self.y = y

        self.rect.x = x
        self.rect.y = y
