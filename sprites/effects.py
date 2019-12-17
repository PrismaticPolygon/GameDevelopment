import pygame as pg
from random import choice, randint
from settings import EFFECTS_LAYER

class MuzzleFlash(pg.sprite.Sprite):

    def __init__(self, game, position, rotation):

        # Game variables

        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Object constants

        self.FLASH_DURATION = 40
        self.IMAGES = [pg.image.load(path).convert_alpha() for path in [
            "assets/images/muzzle_01.png",
            "assets/images/muzzle_02.png",
            "assets/images/muzzle_03.png",
            "assets/images/muzzle_04.png",
            "assets/images/muzzle_05.png"]
        ]

        # Object variables

        size = randint(20, 50)
        self.position = position

        self.spawn_time = pg.time.get_ticks()

        # Image variables

        self.image = pg.transform.scale(choice(self.IMAGES), (size, size))
        self.image = pg.transform.rotate(self.image, rotation)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):

        if pg.time.get_ticks() - self.spawn_time > self.FLASH_DURATION:

            self.kill()