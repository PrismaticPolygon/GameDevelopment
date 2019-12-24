import pygameMenu
import settings

def menu_background():

    pass

def change_difficulty(text, value):

    settings.DIFFICULTY = value

def change_music(text, value):

    settings.MUSIC_ENABLED = value

def create_menu(surface):

    width = settings.WIDTH
    height = settings.HEIGHT
    font = pygameMenu.font.FONT_NEVIS
    bgfun = menu_background
    color = settings.LIGHTGREY  # Background color

    # SETTINGS

    difficulties = [("Easy", 0.75), ("Normal", 1), ("Hard", 1.25)]
    music = [("On", True), ("Off", False)]

    settings_menu = pygameMenu.Menu(surface, width, height, font, "Settings", dopause=True, bgfun=bgfun, menu_color=color)

    settings_menu.add_selector('Difficulty', difficulties, default=1, onchange=change_difficulty, onreturn=change_difficulty)

    settings_menu.add_selector('Music', music, default=1, onchange=change_music, onreturn=change_music)

    # CONTROLS

    controls_menu = pygameMenu.TextMenu(surface, width, height, font, "Controls", dopause=True, bgfun=bgfun, menu_color=color)

    controls = [
        "Use WASD or the arrow keys to move",
        "Use SPACE to shoot",
        "Use R to reload",
        "Use E to equip weapons",
    ]

    for line in controls:

        controls_menu.add_line(line)

    # MAIN

    menu = pygameMenu.Menu(surface, width, height, font, "ffgt86",
                           dopause=True,
                           bgfun=bgfun,
                           menu_color=color,
                           onclose=pygameMenu.events.CLOSE,
                           enabled=True)

    menu.add_option("Play", pygameMenu.events.CLOSE)

    menu.add_option(controls_menu.get_title(), controls_menu)
    menu.add_option(settings_menu.get_title(), settings_menu)
    menu.add_option('Exit', pygameMenu.events.EXIT)  # Add exit function

    return menu