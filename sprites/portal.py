import pygame as pg
from settings import PLAYER_LAYER, MAX_MOBS, DIFFICULTY
from sprites import Zombie
import random
import math

vec = pg.math.Vector2


class Portal(pg.sprite.Sprite):

    def __init__(self, game, x, y):

        # Game variables

        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Portal constants

        self.ROTATION_SPEED = 100 * DIFFICULTY
        self.position = vec(x, y)
        self.rotation = 0
        self.HIT_RECT = pg.Rect(0, 0, 128, 128)
        self.SPAWN_RATE = 5000 / DIFFICULTY
        self.RADIUS = 128
        self.SIZE = 128

        # Portal variables

        self.rotation_speed = 8 * DIFFICULTY
        self.last_spawned = 0

        # Image variables

        self.original_image = pg.image.load("assets/images/portal.png").convert_alpha()
        self.original_image = pg.transform.scale(self.original_image, (self.SIZE, self.SIZE))
        self.image = self.original_image.copy()

        self.image = pg.transform.scale(self.image, (self.SIZE, self.SIZE))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.hit_rect = self.HIT_RECT
        self.hit_rect.center = self.rect.center

    def update(self):

        # Spawn zombies periodically in a circular distribution around the portal
        # https://programming.guide/random-point-within-circle.html
        # https://stackoverflow.com/questions/30564015/how-to-generate-random-points-in-a-circular-distribution

        circle_x, circle_y = self.rect.center

        a = random.random() * 2 * math.pi
        r = self.RADIUS * math.sqrt(random.random())

        x = r * math.cos(a) + circle_x
        y = r * math.sin(a) + circle_y

        now = pg.time.get_ticks()

        if now - self.last_spawned > self.SPAWN_RATE and len(self.game.mobs) < MAX_MOBS:

            Zombie(self.game, x, y)

            self.last_spawned = now

        # Rotate ominously

        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360

        self.image = pg.transform.rotate(self.original_image, self.rotation)

        self.rect = self.image.get_rect()

        self.rect.center = self.position

        self.hit_rect.centerx = self.position.x

        self.hit_rect.centery = self.position.y
