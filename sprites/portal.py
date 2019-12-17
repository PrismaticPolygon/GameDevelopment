from sprites.weapons import Pistol, WeaponMode, Shotgun
from itertools import chain
from random import random, choice
import pygame as pg
from os import path
from settings import PLAYER_LAYER
from sprites.obstacle import collide_with_walls

vec = pg.math.Vector2


class Portal(pg.sprite.Sprite):

    def __init__(self, game, x, y):

        # Game variables

        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Player constants

        self.ROTATION_SPEED = 100
        self.position = vec(x, y)
        self.rotation = 0
        self.HIT_RECT = pg.Rect(0, 0, 128, 128)

        # Portal variables

        self.rotation_speed = 0

        # Image variables

        self.original_image = pg.image.load("assets/images/portal.jpg").convert_alpha()
        self.image = self.original_image.copy()

        self.image = pg.transform.scale(self.image, (128, 128))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.hit_rect = self.HIT_RECT
        self.hit_rect.center = self.rect.center

    def update(self):

        pass

        # self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360
        #
        # self.image = pg.transform.rotate(self.original_image, self.rotation)
        #
        # self.rect = self.image.get_rect()
        # self.rect.center = self.position
        #
        # self.hit_rect.centerx = self.position.x
        #
        # self.hit_rect.centery = self.position.y
        #
        # self.rect.center = self.hit_rect.center
