import pygame as pg
from random import random, choice, randint
from sprites.player import collide_with_walls
from settings import GREEN, RED, YELLOW, SOUND_PATH
from os import path

vec = pg.math.Vector2

class Zombie(pg.sprite.Sprite):

    def __init__(self, game, x, y):

        # Game variables

        # self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        self.game = game

        pg.sprite.Sprite.__init__(self, self.groups)

        # Sprite constants

        self.HEALTH = 20
        self.SPEEDS = [150, 100, 75, 125]
        self.HIT_RECT = pg.Rect(0, 0, 30, 30)
        self.DAMAGE = 10
        self.KNOCKBACK = 20
        self.AVOID_RADIUS = 50
        self.DETECT_RADIUS = 400

        self.SOUNDS = [pg.mixer.Sound(path.join(SOUND_PATH, file)) for file in [
            "brains_1.wav",
            "brains_2.wav",
            "zombie-roar-1.wav",
            "zombie-roar-2.wav",
            "zombie-roar-3.wav",
            "zombie-roar-4.wav",
            "zombie-roar-5.wav",
            "zombie-roar-6.wav",
            "zombie-roar-7.wav",
            "zombie-roar-8.wav"
        ]]

        for sound in self.SOUNDS:

            sound.set_volume(0.2)

        self.DEATH_SOUND = pg.mixer.Sound(path.join(SOUND_PATH, "splat.wav"))

        self.DEATH_IMAGE = pg.image.load("assets/images/splat.png").convert_alpha()
        self.DEATH_IMAGE = pg.transform.scale(self.DEATH_IMAGE, (64, 64))

        # Sprite variables

        self.position = vec(x, y)
        self.velocity = vec(0, 0)
        self.acceleration = vec(0, 0)
        self.rotation = randint(0, 360)
        self.target = game.player

        self.health = self.HEALTH
        self.speed = choice(self.SPEEDS)

        # Image variables

        self.original_image = pg.image.load("assets/images/zombie.png")
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.hit_rect = self.HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        self.rect.center = (x, y)

        self.rect.center = self.position

    def draw_health(self):

        if self.health * 100 > 66:

            color = GREEN

        elif self.health * 100 > 33:

            color = YELLOW

        else:

            color = RED

        width = int(self.rect.width * self.health / self.HEALTH) * 100

        self.health_bar = pg.Rect(0, 0, width, 10)

        if self.health < self.HEALTH:

            pg.draw.rect(self.image, color, self.health_bar)

    def avoid_mobs(self):

        for mob in self.game.mobs:

            if mob != self:

                dist = self.position - mob.position   # Calculate distances between mobs

                if 0 < dist.length() < self.AVOID_RADIUS:

                    self.acceleration += dist.normalize()    # Make it a length of 1.

    def update(self):

        target_dist = self.target.position - self.position

        if target_dist.length_squared() < self.DETECT_RADIUS ** 2:

            if random() < 0.002:

                choice(self.SOUNDS).play()

            self.rotation = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.original_image, self.rotation)

            self.rect = self.image.get_rect()
            self.rect.center = self.position

            self.acceleration = vec(1, 0).rotate(-self.rotation)

            self.avoid_mobs()

            try:

                self.acceleration.scale_to_length(self.speed)

            except ValueError:

                pass

            self.acceleration += self.velocity * -1

            self.velocity += self.acceleration * self.game.dt
            self.position += self.velocity * self.game.dt + 0.5 * self.acceleration * self.game.dt ** 2

            self.hit_rect.centerx = self.position.x

            collide_with_walls(self, self.game.walls, 'sprites')

            self.hit_rect.centery = self.position.y

            collide_with_walls(self, self.game.walls, 'y')

            self.rect.center = self.hit_rect.center

        if self.health <= 0:

            self.DEATH_SOUND.play()

            self.game.map_img.blit(self.DEATH_IMAGE, self.position - vec(32, 32))

            self.kill()