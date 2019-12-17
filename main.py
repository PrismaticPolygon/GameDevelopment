import sys
import pygame as pg
from settings import *
from tilemap import Camera, TiledMap
from sprites import *
from hud import draw_player_health, draw_text

class Game:

    def __init__(self):

        pg.mixer.pre_init(44100, -16, 1, 2048)

        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))

        pg.display.set_caption(TITLE)

        self.clock = pg.time.Clock()

        pg.key.set_repeat(500, 100)

        self.load_data()

        self.night = False
        self.paused = False

    def load_data(self):

        self.title_font = "assets/fonts/ZOMBIE.TTF"
        self.hud_font = "assets/fonts/Impacted2.0.TTF"

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.map = TiledMap("level1")
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)

        self.light_mask = pg.image.load(LIGHT_MASK)
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        pg.mixer.music.load(BG_MUSIC)

    def new(self):

        self.all_sprites = pg.sprite.LayeredUpdates()

        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        self.weapons = pg.sprite.Group()

        self.map = TiledMap("level1")
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

            if tile_object.name == "qbit":

                QBitItem(self, center)

            if tile_object.name == "portal":

                self.portal = Portal(self, center.x, center.y)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False

        # self.effect_sounds["level_start"].play()

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

        self.all_sprites.update()

        self.camera.update(self.player)

        if len(self.mobs) == 0:

            self.playing = False

        # Player hits items

        items = pg.sprite.spritecollide(self.player, self.items, False)

        for item in items:

            if isinstance(item, MedkitItem) and self.player.health < 100:

                self.player.add_health(item.AMOUNT)

            if isinstance(item, ShotgunItem):

                self.player.weapon = Shotgun(self, self.player.position.x, self.player.position.y, self.player.rotation)

            if isinstance(item, QBitItem):

                self.player.qbit_count += 1

            item.pickup()

        # Player hits portal

        if collide_hit_rect(self.player, self.portal) and self.player.qbit_count == NUMBER_OF_QBITS:

            print("The game has been won!")

            self.portal.kill()

        # Mob hits player

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)

        for hit in hits:

            self.player.health -= 10

            hit.vel = vec(0, 0)

            if self.player.health <= 0:

                self.playing = False

        if hits:

            print(hits)

            self.player.position += vec(20, 0).rotate(-hits[0].rotation)

            self.player.hit()

        # Bullets hit mobs

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)

        for mob in hits:

            for bullet in hits[mob]:

                mob.health -= bullet.damage

            mob.vel = vec(0, 0)

    def render_fog(self):

        # Draw the light mask (gradient) onto the fog image.

        self.fog.fill(NIGHT_COLOR)

        self.light_rect.center = self.camera.apply(self.player).center

        self.fog.blit(self.light_mask, self.light_rect)

        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    # Of course, it's more of a structure than a item, but hey ho. We'll just scale it to be massive.

    def draw(self):

        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:

            if isinstance(sprite, Zombie):

                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.night:

            self.render_fog()

        # HUD

        draw_player_health(self.screen, 10, 10, self.player.health / 100)
        draw_text(self.screen, 'Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")

        draw_text(self.screen, 'Q-bits: {}'.format(self.player.qbit_count), self.hud_font, 30, WHITE, WIDTH - 170, 10, align="ne")

        if self.paused:

            self.screen.blit(self.dim_screen, (0, 0))
            draw_text(self.screen, "Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")

        pg.display.flip()

    def events(self):

        # catch all events here
        for event in pg.event.get():

            if event.type == pg.QUIT:

                self.quit()

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:

                    self.quit()

                if event.key == pg.K_p:

                    self.paused = not self.paused

                if event.key == pg.K_n:

                    self.night = not self.night

                if event.key == pg.K_r:

                    self.player.reload()

                if event.key == pg.K_SPACE:

                    self.player.fire()

            if event.type == pg.KEYUP and event.key == pg.K_SPACE:

                self.player.stop_firing()

    def show_start_screen(self):

        pass

    def show_go_screen(self):

        self.screen.fill(BLACK)
        draw_text(self.screen, "GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
        draw_text(self.screen, "Press a key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")

        pg.display.flip()

        self.wait_for_key()

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

# create the game object
g = Game()

g.show_start_screen()

while True:

    g.new()
    g.run()
    g.show_go_screen()