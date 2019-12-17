import sys
import pygame as pg
from settings import *
from os import path
from tilemap import Camera, TiledMap
from random import choice, randint, random

from sprites import Obstacle, Item, collide_hit_rect
from x import *

def draw_player_health(surf, x, y, pct):

    if pct < 0:

        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 20

    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)

    fill_rect = pg.Rect(x, y, int(fill), BAR_HEIGHT)

    if pct > 0.66:

        color = GREEN

    elif pct > 0.33:

        color = YELLOW

    else:

        color = RED

    pg.draw.rect(surf, color, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

class Game:

    def __init__(self):

        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()

        pg.key.set_repeat(500, 100)

        self.load_data()

    def load_data(self):

        game_folder = path.dirname(__file__)

        img_folder = path.join(game_folder, "assets", "PNG", "Man Blue")

        wall_img_path = path.join(game_folder, "assets", "PNG", "Tiles", WALL_IMG)
        zombie_img_path = path.join(game_folder, "assets", "PNG", "Zombie 1", MOB_IMG)
        bullet_img_path = path.join(game_folder, BULLET_IMG)

        self.title_font = path.join(game_folder, "assets", "ZOMBIE.TTF")

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.map = TiledMap("level1")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(wall_img_path).convert_alpha()    # No ned to scale.
        self.mob_img = pg.image.load(zombie_img_path).convert_alpha()    # No ned to scale.
        self.bullet_img = pg.image.load(bullet_img_path)

        self.splat = pg.image.load("assets/splat green.png").convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))

        self.item_images = dict()

        for item in ITEM_IMAGES:

            self.item_images[item] = pg.image.load(path.join(game_folder, ITEM_IMAGES[item])).convert_alpha()

            self.item_images[item] = pg.transform.scale(self.item_images[item], (32, 32))

        self.gun_flashes = list()

        for img in MUZZLE_FLASHES:

            self.gun_flashes.append(pg.image.load(path.join(game_folder, img)).convert_alpha())

        # Sound loading

        pg.mixer.music.load(BG_MUSIC)

        self.effect_sounds = dict()

        for type in EFFECT_SOUNDS:

            self.effect_sounds[type] = pg.mixer.Sound(EFFECT_SOUNDS[type])

        self.weapon_sounds = dict()

        self.weapon_sounds["gun"] = []

        for snd in WEAPON_SOUNDS_GUN:

            self.weapon_sounds["gun"].append(pg.mixer.Sound(snd))

        self.zombie_moan_sounds = []

        for snd in ZOMBIE_MOAN_SOUNDS:

            sound = pg.mixer.Sound(snd)
            sound.set_volume(0.2)

            self.zombie_moan_sounds.append(sound)

        self.player_hit_sounds = []

        for snd in PLAYER_HIT_SOUNDS:

            self.player_hit_sounds.append(pg.mixer.Sound(snd))

        self.zombie_hit_sounds = []

        for snd in ZOMBIE_HIT_SOUNDS:

            self.zombie_hit_sounds.append(pg.mixer.Sound(snd))

        # Resize if necessary.

    def new(self):
        # initialize all variables and do all the setup for a new game

        self.all_sprites = pg.sprite.LayeredUpdates()

        self.paused = False

        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        self.weapons = pg.sprite.Group()

        # Aha. It tries to draw it! That's reassuring.
        # The image will depend on whether we've got it equipped or not.

        for tile_object in self.map.tmxdata.objects:

            center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)

            row = tile_object.y
            col = tile_object.x

            if tile_object.name == "player":

                self.player = Player(self, center.x, center.y)

            if tile_object.name == "wall":

                Obstacle(self, col, row, tile_object.width, tile_object.height)

            if tile_object.name == "zombie":

                Zombie(self, center.x, center.y)

            if tile_object.name in ["health"]:

                Item(self, center, tile_object.name)




        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

        # self.effect_sounds["level_start"].play()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self):

        # game loop - set self.playing = False to end the game

        self.playing = True

        # pg.mixer.music.play(loops=-1)

        while self.playing:

            self.dt = self.clock.tick(FPS) / 1000

            self.events()

            if not self.paused:

                self.update()

            self.draw()

    def quit(self):

        pg.quit()
        sys.exit()

    def update(self):

        # update portion of the game loop
        self.all_sprites.update()

        self.camera.update(self.player)

        # Player hits items

        hits = pg.sprite.spritecollide(self.player, self.items, False)

        for hit in hits:

            if hit.type == "health" and self.player.health < PLAYER_HEALTH:

                self.effect_sounds["health_up"].play()

                self.player.add_health(HEALTH_PACK_AMOUNT)

                hit.kill()

        # Mob hits player

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)

        for hit in hits:

            if random() < 0.7:

                choice(self.player_hit_sounds).play()

            self.player.health -= MOB_DAMAGE

            hit.vel = vec(0, 0)

            if self.player.health <= 0:

                self.playing = False

        if hits:

            self.player.position += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rotation)

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)

        for hit in hits:

            hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

        # Bullets disappear when they hit the zombie, but the zombies don't.

    def draw_grid(self):

        for x in range(0, WIDTH, TILESIZE):

            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, TILESIZE):

            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):

        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        # self.screen.fill(BGCOLOR)
        # self.draw_grid()

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:

            if isinstance(sprite, Zombie):

                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))

            if self.draw_debug:

                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)

        if self.draw_debug:

            for wall in self.walls:

                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)


        # HUD

        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        # self.all_sprites.draw(self.screen)

        if self.paused:

            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        pg.display.flip()

    def events(self):

        # catch all events here
        for event in pg.event.get():

            if event.type == pg.QUIT:

                self.quit()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    self.quit()

                if event.key == pg.K_h:

                    self.draw_debug = not self.draw_debug

                if event.key == pg.K_p:

                    self.paused = not self.paused

                if event.key == pg.K_r:

                    self.player.reload()

                if event.key == pg.K_SPACE:

                    self.player.fire()

            if event.type == pg.KEYUP and event.key == pg.K_SPACE:

                self.player.stop_firing()

    def show_start_screen(self):

        pass

    def show_go_screen(self):

        pass


# create the game object
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()
    g.show_go_screen()