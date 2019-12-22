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
TITLE = "Zombitch!"

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

BG_MUSIC = "assets/music/espionage.ogg"
LEVEL_START = "assets/sounds/level_start.wav"

NUMBER_OF_QBITS = 1
MAX_MOBS = 50