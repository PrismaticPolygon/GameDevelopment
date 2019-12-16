import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings

PLAYER_SPEED = 280
PLAYER_IMG = "manBlue_hold.png"
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
PLAYER_HEALTH = 100

WALL_IMG = "tile_96.png"

# Gun settings

BULLET_IMG = "assets/PNG/weapon_gun.png"
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
GUN_SPREAD = 5
KICKBACK = 200
BULLET_DAMAGE = 10

# Mob settings

MOB_IMG = "zoimbie1_hold.png"

MOB_SPEEDS = [150, 100, 75, 125]

MOB_SPEED = 150
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

MUZZLE_FLASHES = [
    "assets/PNG (Transparent)/muzzle_01.png",
    "assets/PNG (Transparent)/muzzle_02.png",
    "assets/PNG (Transparent)/muzzle_03.png",
    "assets/PNG (Transparent)/muzzle_04.png",
    "assets/PNG (Transparent)/muzzle_05.png"
]

FLASH_DURATION = 40

# LAYERS

WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# ITEMS
ITEM_IMAGES = {"health": "assets/healthpack.png"}

HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.3

# SOUND

BG_MUSIC = "assets/sounds/music/espionage.ogg"

PLAYER_HIT_SOUNDS = [
    "assets/sounds/snd/pain/8.wav",
    "assets/sounds/snd/pain/9.wav",
    "assets/sounds/snd/pain/10.wav",
    "assets/sounds/snd/pain/11.wav",
    "assets/sounds/snd/pain/12.wav",
    "assets/sounds/snd/pain/13.wav",
    "assets/sounds/snd/pain/14.wav"
]

ZOMBIE_MOAN_SOUNDS = [
    "assets/sounds/snd/brains2.wav",
    "assets/sounds/snd/brains3.wav",
    "assets/sounds/snd/zombie-roar-1.wav",
    "assets/sounds/snd/zombie-roar-2.wav",
    "assets/sounds/snd/zombie-roar-3.wav",
    "assets/sounds/snd/zombie-roar-4.wav",
    "assets/sounds/snd/zombie-roar-5.wav",
    "assets/sounds/snd/zombie-roar-6.wav",
    "assets/sounds/snd/zombie-roar-7.wav",
    "assets/sounds/snd/zombie-roar-8.wav"
]

ZOMBIE_HIT_SOUNDS = ["assets/sounds/snd/splat-15.wav"]

WEAPON_SOUNDS_GUN = ["assets/sounds/snd/sfx_weapon_singleshot2.wav"]

EFFECT_SOUNDS = {
    "level_start": "assets/sounds/snd/level_start.wav",
    "health_up": "assets/sounds/snd/health_pack.wav"
}