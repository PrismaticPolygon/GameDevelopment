import pygame as pg
import pytmx
from os import path
from settings import WIDTH, HEIGHT

# Let's think. I've got the loading working. I haven't really got level traversal working, but I don't think that that
# will be too hard. We want a MVP. That's it. SO: I want to fix the images of the items that I do have.

class TiledMap:

    def __init__(self, filename):

        tm = pytmx.load_pygame(path.join("maps", filename  + ".tmx"), pixelalpha=True)

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