import sys
import pygame as pg
import settings
from settings import *
from tilemap import Camera, TiledMap
from sprites import *
from hud import draw_player_health, draw_text
from menu import create_menu

WIDTH = settings.WIDTH
HEIGHT = settings.HEIGHT
TITLE = settings.TITLE

# Not sure that I can be arsed, to be honest. Hold up. I WILL submit this this evening. Which means I can dedicate all
# of today doing it.

class Game:

    def __init__(self):

        pg.mixer.pre_init(44100, -16, 1, 2048)

        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()

        pg.key.set_repeat(500, 100)

        self.player = None
        self.portal = None
        self.NUMBER_OF_QBITS = 0

        self.load_data()

        self.night = True
        self.paused = False
        self.playing = True
        self.dt = 0
        self.last_dt = 1

        self.victory = False

        self.can_equip = False

        self.menu = create_menu(self.screen)

    def load_data(self):

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 140))

        self.map = TiledMap("science_site")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)

        self.light_mask = pg.image.load(LIGHT_MASK)
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        pg.mixer.music.load(BG_MUSIC)

    def new(self):

        global DIFFICULTY

        self.all_sprites = pg.sprite.LayeredUpdates()

        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        self.weapons = pg.sprite.Group()

        self.map = TiledMap("science_site")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        for tile_object in self.map.tmxdata.objects:

            center = vec(float(tile_object.x) + float(tile_object.width) / 2,
                         float(tile_object.y) + float(tile_object.height) / 2)

            row = float(tile_object.y)
            col = float(tile_object.x)

            if tile_object.name == "player":

                self.player = Player(self, center.x, center.y)

            if tile_object.name == "wall":

                Obstacle(self, col, row, float(tile_object.width), float(tile_object.height))

            if tile_object.name == "zombie":

                Zombie(self, center.x, center.y)

            if tile_object.name == "health":

                MedkitItem(self, center)

            if tile_object.name == "shotgun":

                ShotgunItem(self, center)

            if tile_object.name == "pistol":

                PistolItem(self, center)

            if tile_object.name == "sniper":

                PistolItem(self, center)

            if tile_object.name == "rifle":

                AssaultRifleItem(self, center)

            if tile_object.name == "qbit":

                QBitItem(self, center)

                self.NUMBER_OF_QBITS += 1
                DIFFICULTY += 0.1

            if tile_object.name == "portal":

                self.portal = Portal(self, center.x, center.y)

        self.camera = Camera(self.map.width, self.map.height)

        # self.effect_sounds["level_start"].play()

    def run(self):

        if settings.MUSIC_ENABLED:

            pg.mixer.music.play(loops=-1) # Play background music on a loop

        while self.playing:

            self.dt = min(self.clock.tick(FPS) / 1000, self.last_dt)   # To prevent the massive dt on menu pause

            events = pg.event.get()

            for event in events:

                if event.type == pg.QUIT:

                    self.quit()

                if event.type == pg.KEYDOWN:

                    if event.key == pg.K_ESCAPE:

                        self.menu.enable()

                        self.last_dt = self.dt

                    if event.key == pg.K_n:

                        self.night = not self.night

                    if event.key == pg.K_r:

                        self.player.reload()

                    if event.key == pg.K_SPACE:

                        self.player.fire()

                if event.type == pg.KEYUP:

                    if event.key == pg.K_SPACE:

                        self.player.stop_firing()

                    if event.key == pg.K_e:

                        self.player.equip_weapon()

            self.menu.mainloop(events)

            self.draw()

            self.update()

    def quit(self):

        pg.quit()
        sys.exit()

    def update(self):

        self.all_sprites.update()

        self.camera.update(self.player)

        items = pg.sprite.spritecollide(self.player, self.items, False)

        for item in items:

            if isinstance(item, MedkitItem) and self.player.health < 100:

                self.player.add_health(item.AMOUNT)

                item.pickup()

            elif isinstance(item, QBitItem):

                self.player.qbit_count += 1

                item.pickup()

        # Player hits portal

        if self.portal is not None:

            if collide_hit_rect(self.player, self.portal) and self.player.qbit_count == self.NUMBER_OF_QBITS:
            # if collide_hit_rect(self.player, self.portal):

                self.portal.kill()

                # Then, after 5 seconds, set playing to false.

                for mob in self.mobs:

                    mob.kill()



                self.playing = False

                self.victory = True

        # Mob hits player

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)

        for hit in hits:

            self.player.health -= 10

            hit.vel = vec(0, 0)

            if self.player.health <= 0:

                self.playing = False

        if hits:

            self.player.position += vec(20, 0).rotate(-hits[0].rotation)

            self.player.hit()

        # Bullets hit mobs

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, False)

        for mob in hits:

            for bullet in hits[mob]:

                mob.health -= bullet.DAMAGE

                if not isinstance(self.player.weapon, SniperRifle):

                    bullet.kill()

            mob.vel = vec(0, 0)

    def render_fog(self):

        # Draw the light mask (gradient) onto the fog image.

        self.fog.fill(NIGHT_COLOR)

        self.light_rect.center = self.camera.apply(self.player).center

        self.fog.blit(self.light_mask, self.light_rect)

        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):

        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        # Hm. It seems there is a Pistol lying around...

        for sprite in self.all_sprites:

            if isinstance(sprite, Zombie):

                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.night:

            self.render_fog()

        # HUD

        draw_player_health(self.screen, 10, 10, self.player.health / 100)
        draw_text(self.screen, 'Zombies: {}'.format(len(self.mobs)), "hud", 30, WHITE, WIDTH - 10, 10, align="ne")

        weapon = self.player.can_equip_weapon()

        if weapon is not None:

            draw_text(self.screen, "Press E to equip {}".format(weapon), "hud", 30, WHITE, WIDTH / 2, HEIGHT * 4 / 5, align="center")

        if self.player.needs_to_reload():

            draw_text(self.screen, "Press R to reload", "hud", 30, WHITE, WIDTH / 2, HEIGHT * 4 / 5, align="center")

        if self.player.is_reloading():

            draw_text(self.screen, "Reloading...", "hud", 30, WHITE, WIDTH / 2, HEIGHT * 4 / 5, align="center")

        draw_text(self.screen, 'Q-bits: {} / {}'.format(self.player.qbit_count, self.NUMBER_OF_QBITS),
                  "hud", 30, WHITE, WIDTH - 200, 10, align="ne")

        if self.paused:

            self.screen.blit(self.dim_screen, (0, 0))
            draw_text(self.screen, "Paused", "title", 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        pg.display.flip()

    def show_start_screen(self):

        while self.menu.is_enabled():

            self.screen.fill(BLACK)

            events = pg.event.get()

            self.menu.mainloop(events)

    def show_win_screen(self):

        self.screen.fill(BLACK)
        draw_text(self.screen, "You win!", "title", 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(self.screen, "Press a key to start", "title", 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()

        # self.wait_for_key()

    def show_go_screen(self):

        self.screen.fill(BLACK)
        draw_text(self.screen, "GAME OVER", "title", 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(self.screen, "Press a key to start", "title", 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()

        # self.wait_for_key()

    def wait_for_key(self):

        pg.event.wait()
        waiting = True

        while waiting:

            self.clock.tick(FPS)

            for event in pg.event.get():

                if event.type == pg.QUIT:

                    waiting = False
                    self.quit()

                if event.type == pg.KEYUP:

                    waiting = False

while True:

    g = Game()

    g.new()
    g.show_start_screen()
    g.run()

    if g.victory:

        g.show_win_screen()

    else:

        g.show_go_screen()

    g.wait_for_key()