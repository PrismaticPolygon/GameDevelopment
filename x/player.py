from x.weapons import Pistol, WeaponMode
import pygame as pg
from os import path

vec = pg.math.Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):

        # Game variables

        # self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # Player constants

        self.SPEED = 280
        self.IMG = "manBlue_hold.png"
        self.ROTATION_SPEED = 250
        self.HIT_RECT = pg.Rect(0, 0, 35, 35)
        self.BARREL_OFFSET = vec(30, 10)
        self.HEALTH = 100

        # Player variables

        self.velocity = vec(0, 0)
        self.position = vec(x, y)
        self.rotation = 0

        self.health = self.HEALTH
        self.weapon = Pistol(game, x, y, self.rotation)
        self.rotation_speed = 0
        self.is_firing = False

        # Image variables

        self.original_image = pg.image.load(path.join("assets", "images", "player", "manBlue_hold.png")).convert_alpha()
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.hit_rect = self.HIT_RECT
        self.hit_rect.center = self.rect.center

    def fire(self):
        """
        Called on the K_SPACE KEYDOWN event. If the weapon is semi-automatic, fire once. If it is automatic, set the
        is_firing flag to True. When this is True, the player fires a new projectile when update is called.
        :return:
        """

        if self.weapon.MODE == WeaponMode.SEMI_AUTOMATIC:

            self.weapon.fire()

        else:

            self.is_firing = True

    def stop_firing(self):
        """
        Called on the K_SPACE KEYUP event. Sets the is_firing flag to False, which stops the player firing new
        projectiles when update is called.
        :return:
        """

        self.is_firing = False

    def get_keys(self):

        # Keydown gives keys which are pressed down on that frame.

        self.velocity = vec(0, 0)
        self.rotation_speed = 0

        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:

            self.rotation_speed = self.ROTATION_SPEED

        if keys[pg.K_RIGHT] or keys[pg.K_d]:

            self.rotation_speed = -self.ROTATION_SPEED

        if keys[pg.K_UP] or keys[pg.K_w]:

            self.velocity = vec(self.SPEED, 0).rotate(-self.rotation)

        if keys[pg.K_DOWN] or keys[pg.K_s]:

            self.velocity = vec(-self.SPEED / 2, 0).rotate(-self.rotation)


    def reload(self):

        self.weapon.reload()

    def add_health(self, amount):

        self.health += amount

        if self.health > self.HEALTH:

            self.health = self.HEALTH

    def update(self):

        self.get_keys()

        self.rotation = (self.rotation + self.rotation_speed * self.game.dt) % 360

        self.image = pg.transform.rotate(self.game.player_img, self.rotation)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

        self.position += self.velocity * self.game.dt

        self.hit_rect.centerx = self.position.x

        # self.rect.centerx = self.pos.x

        collide_with_walls(self, self.game.walls, 'x')

        self.hit_rect.centery = self.position.y

        collide_with_walls(self, self.game.walls, 'y')

        self.rect.center = self.hit_rect.center

        # Update weapon

        self.weapon.rotation = self.rotation
        self.weapon.position = self.position + self.BARREL_OFFSET.rotate(-self.rotation)

        if self.is_firing:

            self.weapon.fire()


def collide_with_walls(sprite, group, dir):

    if dir == 'x':

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