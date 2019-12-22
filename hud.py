import pygame as pg
from settings import GREEN, YELLOW, WHITE, RED

fonts = {
    "title": "assets/fonts/ZOMBIE.TTF",
    "hud": "assets/fonts/Impacted2.0.TTF"
}

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

def draw_text(screen, text, font_name, size, color, x, y, align="nw"):

    font = pg.font.Font(fonts[font_name], size)

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

    screen.blit(text_surface, text_rect)

def draw_player_ammo(surf, x, y, weapon):

    pass

# Display the user's health
# Display the user's ammo
