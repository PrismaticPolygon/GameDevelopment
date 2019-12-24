import pygame as pg
from os import path
vec = pg.math.Vector2

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# Game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "ffgt86"

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "assets/lighting/light_350_med.png"

# Layers

WALL_LAYER = 1
ITEMS_LAYER = 1

PLAYER_LAYER = 2
MOB_LAYER = 2

BULLET_LAYER = 3
WEAPON_LAYER = 3

EFFECTS_LAYER = 4

# SOUND

root = path.dirname(__file__)

SOUND_PATH = path.join(root, "assets", "sounds")
MUSIC_PATH = path.join(root, "assets", "music")
IMAGE_PATH = path.join(root, "assets", "images")

BG_MUSIC = "assets/music/espionage.ogg"
LEVEL_START = "assets/sounds/level_start.wav"

NUMBER_OF_QBITS = 0
MAX_MOBS = 50
DIFFICULTY = 1

def aspect_scale(img, bx, by):

    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by

    return pg.transform.scale(img, (int(sx), int(sy)))

    # Why is that old iamge left?