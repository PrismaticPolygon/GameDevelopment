import pygame as pg
from settings import TILESIZE, WIDTH, HEIGHT

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

    def update(self, target):

        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size

        x = min(0, x)                       # Left
        y = min(0, y)                       # Top

        x = max(-(self.width - WIDTH), x)   # Right
        y = max(-(self.height - HEIGHT), y) # Bottom

        self.camera = pg.Rect(x, y, self.width, self.height)