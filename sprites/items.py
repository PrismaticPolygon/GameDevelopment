import pygame as pg
from os import path
from settings import ITEMS_LAYER, aspect_scale, IMAGE_PATH, SOUND_PATH
import pytweening as tween

class Item(pg.sprite.Sprite):

    def __init__(self, game, position, image, sound):

        # Game variables

        self.layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Item constants

        self.BOB_RANGE = 15
        self.BOB_SPEED = 0.3

        # Item variables

        self.step = 0
        self.dir = 1
        self.pickup_sound = pg.mixer.Sound(path.join(SOUND_PATH, sound))

        self.position = position

        # Image variables

        self.image = pg.image.load(path.join(IMAGE_PATH, image)).convert_alpha()
        self.image = aspect_scale(self.image, 32, 32)


        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):

        offset = self.BOB_RANGE * (tween.easeInOutSine(self.step / self.BOB_RANGE) - 0.5)

        self.rect.centery = self.position.y + offset * self.dir

        self.step += self.BOB_SPEED

        if self.step > self.BOB_RANGE:

            self.step = 0
            self.dir *= -1

    def pickup(self):

        self.pickup_sound.play()

        self.kill()

class MedkitItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position, "medkit.png", "health_pack.wav")

        self.AMOUNT = 20

    def __str__(self):

        return "Medkit"

class ShotgunItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position, "shotgun.png", "gun_pickup.wav")

    def __str__(self):

        return "Shotgun"

class PistolItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position, "pistol.png", "gun_pickup.wav")

    def __str__(self):

        return "Pistol"

class SniperRifleItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position, "sniper.png", "gun_pickup.wav")

    def __str__(self):

        return "Sniper Rifle"


class AssaultRifleItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position, "machinegun.png", "gun_pickup.wav")

    def __str__(self):

        return "Assault Rifle"

class QBitItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position, "qbit.png", "gun_pickup.wav")
