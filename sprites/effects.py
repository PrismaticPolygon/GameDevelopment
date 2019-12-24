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
        self.image = pg.transform.rotate(self.image, -90 + rotation)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):

        if pg.time.get_ticks() - self.spawn_time > self.FLASH_DURATION:

            self.kill()

class Explosion(pg.sprite.Sprite):

    def __init__(self, game, center):

        # Game variables

        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Object constants

        self.FLASH_DURATION = 40
        self.IMAGES = [pg.image.load(path).convert_alpha() for path in [
            "assets/images/regularExplosion00.png",
            "assets/images/regularExplosion01.png",
            "assets/images/regularExplosion02.png",
            "assets/images/regularExplosion03.png",
            "assets/images/regularExplosion04.png",
            "assets/images/regularExplosion05.png",
            "assets/images/regularExplosion06.png",
            "assets/images/regularExplosion07.png",
            "assets/images/regularExplosion08.png"]
        ]

        self.IMAGES = [pg.transform.scale(img, (75, 75)) for img in self.IMAGES]
        self.FRAME_RATE = 50

        # Object variables

        self.size = randint(20, 50)
        self.center = center

        self.frame = 0
        self.last_update = pg.time.get_ticks()

        self.spawn_time = pg.time.get_ticks()

        # Image variables

        self.image = self.IMAGES[0]

        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def update(self):

        now = pg.time.get_ticks()

        if now - self.last_update > self.FRAME_RATE:

            self.last_update = now

            self.frame += 1

            if self.frame == len(self.IMAGES):

                self.kill()

            else:

                center = self.rect.center

                self.image = self.IMAGES[self.frame]

                self.rect = self.image.get_rect(center=center)
