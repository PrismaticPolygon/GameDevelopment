import pygame as pg
from settings import ITEMS_LAYER
import pytweening as tween

class Item(pg.sprite.Sprite):

    def __init__(self, game, position):

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
        self.pickup_sound = pg.mixer.Sound("assets/sounds/health_pack.wav")

        self.position = position

        # Image variables

        self.image = pg.image.load("assets/images/medkit.png").convert_alpha()
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

        print("Pickup called")

        self.pickup_sound.play()

        self.kill()

class MedkitItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position)

        self.AMOUNT = 20

        self.image = pg.image.load("assets/images/medkit.png").convert_alpha()
        self.pickup_sound = pg.mixer.Sound("assets/sounds/health_pack.wav")

        self.image = pg.transform.scale(self.image, (32, 32))

class ShotgunItem(Item):

    def __init__(self, game, position):

        Item.__init__(self, game, position)

        self.image = pg.image.load("assets/images/shotgun.png").convert_alpha()
        self.pickup_sound = pg.mixer.Sound("assets/sounds/gun_pickup.wav")

        self.image = pg.transform.scale(self.image, (32, 32))




