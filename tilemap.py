import pygame as pg
from os import path
import pytmx
from settings import TILESIZE, WIDTH, HEIGHT


def collide_hit_rect(one, two):

    return one.hit_rect.colliderect(two.rect)

class TiledMap:

    def __init__(self, filename):

        file_path = path.join("maps", filename  + ".tmx")

        tm = pytmx.load_pygame(file_path, pixelalpha=True)

        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight

        self.tmxdata = tm

    def render(self, surface):

        ti = self.tmxdata.get_tile_image_by_gid

        for layer in self.tmxdata.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer): # Multiple kinds of layer exist (Tile, Object, Image)

                for x, y, gid in layer:

                    tile = ti(gid)

                    if tile:

                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):

        temp_surface = pg.Surface((self.width, self.height))

        self.render(temp_surface)

        return temp_surface

class Map:

    def __init__(self, filename):

        self.data = list()

        with open(filename) as f:

            for line in f:

                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)

        self.width =  self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:

    def __init__(self, width, height):

        self.camera = pg.Rect(0, 0, width, height)

        self.width = width
        self.height = height

    def apply(self, entity):

        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):

        return rect.move(self.camera.topleft)

    def update(self, target):

        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size

        x = min(0, x)                       # Left
        y = min(0, y)                       # Top

        x = max(-(self.width - WIDTH), x)   # Right
        y = max(-(self.height - HEIGHT), y) # Bottom

        self.camera = pg.Rect(x, y, self.width, self.height)