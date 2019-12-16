from enum import Enum
from random import choice, uniform
import pygame as pg
import threading
from x.effects import MuzzleFlash
from os import path

vec = pg.math.Vector2

# Define different classes of weapon, melee and ranged.
# Each ranged weapon has a magaz

# BUT, if we want an original, then that points back to us loading everything in one place.

class WeaponMode(Enum):

    AUTOMATIC = 0
    SEMI_AUTOMATIC = 1

sound_path = path.join("assets", "sound", "weapons")

class Bullet(pg.sprite.Sprite):

    def __init__(self, game, position, direction, velocity):

        # Game variables

        # self._layer = BULLET_LAYER

        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Bullet variables

        self.position = position
        self.direction = direction
        self.velocity = velocity

        # Image variables

        self.image = game.bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = position

    def update(self):

        self.position += self.velocity * self.game.dt
        self.rect.center = self.position

        if pg.sprite.spritecollideany(self, self.game.walls):

            self.kill()

class Firearm(pg.sprite.Sprite):

    def __init__(self, game, x, y, rotation):

        # Game variables

        self.groups = game.all_sprites, game.weapons
        self.game = game

        pg.sprite.Sprite.__init__(self, self.groups)

        # Weapon constants

        self.CAPACITY = 8
        self.MODE = WeaponMode.SEMI_AUTOMATIC
        self.SPEED = 500
        self.SPREAD = 5
        self.KICKBACK = 200
        self.DAMAGE = 10
        self.RATE_OF_FIRE = 150
        self.RELOAD_SPEED = 1000

        # Weapon variables

        self.capacity = self.CAPACITY
        self.last_fired_at = 0
        self.sound = pg.mixer.Sound(path.join(sound_path, "pistol", "shot.wav"))

        self.reload_timer = None

        # Sprite variables

        self.rotation = rotation
        self.position = vec(x, y)

        # Image variables

        self.original_image = pg.image.load(path.join("assets", "PNG", "weapon_silencer.png")).convert_alpha()
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = self.position

    def update(self):

        self.image = pg.transform.rotate(self.original_image, self.rotation)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def cancel_reload(self):

        if self.reload_timer is not None:

            self.reload_timer.cancel()
            self.reload_timer = None

    def reload(self):

        def reload_callback():

            print("Reloaded!")

            self.capacity = self.CAPACITY
            self.reload_timer = None

        if self.reload_timer is None and self.capacity < self.CAPACITY: # Not currently reloading and not a full clip.

            self.reload_timer = threading.Timer(self.RELOAD_SPEED / 1000, reload_callback)
            self.reload_timer.start()  # after self.RELOAD_SPEED / 1000 seconds, 'callback' will be called

class Pistol(Firearm):

    def __init__(self, game, x, y, rotation):

        Firearm.__init__(self, game, x, y, rotation)

        # Weapon-specific constants

        self.CAPACITY = 8
        self.MODE = WeaponMode.SEMI_AUTOMATIC
        self.SPEED = 500
        self.SPREAD = 5
        self.KICKBACK = 200
        self.DAMAGE = 10
        self.RATE_OF_FIRE = 150
        self.RELOAD_SPEED = 1000

        # Weapon-specific variables

        self.image = pg.image.load(path.join("assets", "PNG", "weapon_silencer.png")).convert_alpha()

        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = self.position

    def fire(self):

        if self.capacity > 0 and self.reload_timer is None:

            now = pg.time.get_ticks()

            self.sound.play()
            self.last_fired_at = now
            self.capacity -= 1

            spread = uniform(-self.SPREAD, self.SPREAD)
            direction = vec(1, 0).rotate(-self.rotation)
            velocity = direction.rotate(spread) * self.SPEED

            Bullet(self.game, self.position, direction, velocity)

            MuzzleFlash(self.game, self.position, -self.rotation)

