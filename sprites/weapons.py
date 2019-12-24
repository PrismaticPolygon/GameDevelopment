from enum import Enum
from random import uniform
from os import path
import pygame as pg
import threading
from sprites.effects import MuzzleFlash
from settings import BULLET_LAYER, aspect_scale, IMAGE_PATH, SOUND_PATH

vec = pg.math.Vector2

class WeaponMode(Enum):

    AUTOMATIC = 0
    SEMI_AUTOMATIC = 1

class Bullet(pg.sprite.Sprite):

    def __init__(self, game, rotation, position, velocity, damage, image):

        # Game variables

        self._layer = BULLET_LAYER
        self.game = game
        self.groups = game.all_sprites, game.bullets

        pg.sprite.Sprite.__init__(self, self.groups)

        # Bullet constants

        self.VELOCITY = velocity * uniform(0.9, 1.1)
        self.DAMAGE = damage
        self.ROTATION = rotation
        self.ORIGINAL_IMAGE = pg.image.load(path.join(IMAGE_PATH, image)).convert_alpha()

        # Bullet variables

        self.position = vec(position)

        # Image variables

        self.image = pg.transform.rotate(self.ORIGINAL_IMAGE, -90 + self.ROTATION)
        self.image = aspect_scale(self.image, 8, 8)

        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = position

    def update(self):

        self.position += self.VELOCITY * self.game.dt
        self.rect.center = self.position

        if pg.sprite.spritecollideany(self, self.game.walls):

            self.kill()

class Firearm:

    def __init__(self, game, x, y, rotation, capacity, mode, speed, spread, kickback, damage, rate_of_fire,
                 reload_speed, bullet_count, image, sound, bullet_image):

        # Game variables

        self.game = game

        # Weapon constants

        self.CAPACITY = capacity
        self.MODE = mode
        self.SPEED = speed
        self.SPREAD = spread
        self.KICKBACK = kickback
        self.DAMAGE = damage
        self.RATE_OF_FIRE = rate_of_fire
        self.RELOAD_SPEED = reload_speed
        self.BULLET_COUNT = bullet_count
        self.BULLET_IMAGE = bullet_image

        self.ORIGINAL_IMAGE = pg.image.load(path.join(IMAGE_PATH, image)).convert_alpha()
        self.SOUND = pg.mixer.Sound(path.join(SOUND_PATH, sound))

        # Weapon variables

        self.capacity = self.CAPACITY

        self.last_fired_at = 0
        self.reload_timer = None

        self.rotation = rotation
        self.position = vec(x, y)

    def is_reloading(self):

        return self.reload_timer is not None

    def cancel_reload(self):

        if self.reload_timer is not None:

            self.reload_timer.cancel()
            self.reload_timer = None

    def reload(self):

        def reload_callback():

            self.capacity = self.CAPACITY
            self.reload_timer = None

        if self.reload_timer is None and self.capacity < self.CAPACITY: # Not currently reloading and not a full clip.

            self.reload_timer = threading.Timer(self.RELOAD_SPEED / 1000, reload_callback)
            self.reload_timer.start()  # after self.RELOAD_SPEED / 1000 seconds, 'callback' will be called

    def fire(self):

        now = pg.time.get_ticks()

        if self.capacity > 0 and self.reload_timer is None and self.last_fired_at - now < self.RATE_OF_FIRE:

            if self.SOUND.get_num_channels() > 2:

                self.SOUND.stop()

            self.SOUND.play()

            self.last_fired_at = now
            self.capacity -= 1

            direction = vec(1, 0).rotate(-self.rotation)

            for i in range(self.BULLET_COUNT):

                spread = uniform(-self.SPREAD, self.SPREAD)
                velocity = direction.rotate(spread) * self.SPEED

                Bullet(self.game, self.rotation, self.position, velocity, self.DAMAGE, self.BULLET_IMAGE)

            MuzzleFlash(self.game, self.position, self.rotation)

class Pistol(Firearm):

    def __init__(self, game, x, y, rotation):

        Firearm.__init__(self, game, x, y, rotation, 8, WeaponMode.SEMI_AUTOMATIC, 500, 5, 200, 10, 150,
                         1000, 1, "pistol.png", "pistol.wav", "ammo_pistol.png")

class Shotgun(Firearm):

    def __init__(self, game, x, y, rotation):

        Firearm.__init__(self, game, x, y, rotation, 5, WeaponMode.SEMI_AUTOMATIC, 400, 20, 400, 5, 150,
                         1000, 12, "shotgun.png", "shotgun.wav", "bullet.png")

class RocketLauncher(Firearm):

    def __init__(self, game, x, y, rotation):

        Firearm.__init__(self, game, x, y, rotation, 1, WeaponMode.SEMI_AUTOMATIC, 300, 1, 1000, 0, 400,
                         2000, 1, "rocketlauncher.png", "shotgun.wav", "ammo_rocket.png")

class AssaultRifle(Firearm):

    def __init__(self, game, x, y, rotation):

        Firearm.__init__(self, game, x, y, rotation, 30, WeaponMode.AUTOMATIC, 600, 10, 300, 12, 100,
                         1500, 1, "machinegun.png", "shotgun.wav", "ammo_machinegun.png")

