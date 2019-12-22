# coding=utf-8
"""
pygame-menu
https://github.com/ppizarror/pygame-menu

EXAMPLE - TIMER CLOCK
Example file, timer clock with in-menu options.

License:
-------------------------------------------------------------------------------
The MIT License (MIT)
Copyright 2017-2019 Pablo Pizarro R. @ppizarror

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-------------------------------------------------------------------------------
"""

# Import libraries
import sys

sys.path.insert(0, '../../')

from random import randrange
import datetime
import os
import pygame
import pygameMenu

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------
ABOUT = ['pygameMenu {0}'.format(pygameMenu.__version__),
         'Author: @{0}'.format(pygameMenu.__author__),
         pygameMenu.locals.TEXT_NEWLINE,
         'Email: {0}'.format(pygameMenu.__email__)]
COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
H_SIZE = 600  # Height of window size
HELP = ['Press ESC to enable/disable Menu',
        'Press ENTER to access a Sub-Menu or use an option',
        'Press UP/DOWN to move through Menu',
        'Press LEFT/RIGHT to move through Selectors']
W_SIZE = 800  # Width of window size

surface = None

def mainmenu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """
    global surface
    surface.fill((40, 0, 40))

DIFFICULTY = 1

# Okay. Now we're getting somewhere. I just need to figure out how everything fits together.
# If I wanted, I could auo

def change_difficulty(value, c=None, **kwargs):
    """
    Change background color.

    :param value: Selected option (data, index)
    :type value: tuple
    :param c: Color tuple
    :type c: tuple
    """

    difficulty, _ = value

    if difficulty == "Easy":

        DIFFICULTY = 0.75

    elif difficulty == "Normal":

        DIFFICULTY = 1

    elif difficulty == "Hard":

        DIFFICULTY = 1.25

def main(test=False):
    """
    Main program.

    :param test: Indicate function is being tested
    :type test: bool
    :return: None
    """

    # -------------------------------------------------------------------------
    # Init pygame
    # -------------------------------------------------------------------------
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # Create window
    global surface
    surface = pygame.display.set_mode((W_SIZE, H_SIZE))
    pygame.display.set_caption('Example - Timer Clock')

    settings = pygameMenu.Menu(surface,
                                 dopause=False,
                                 font=pygameMenu.font.FONT_NEVIS,
                                 menu_alpha=85,
                                 menu_color=(0, 0, 0),  # Background color
                                 menu_color_title=(0, 0, 0),
                                 menu_height=int(H_SIZE * 0.65),
                                 menu_width=600,
                                 onclose=pygameMenu.events.RESET,  # If this menu closes (ESC) back to main
                                 option_shadow=True,
                                 rect_width=4,
                                 title='Settings',
                                 title_offsety=5,  # Adds 5px to title vertical position
                                 window_height=H_SIZE,
                                 window_width=W_SIZE
                                 )

    settings.add_selector('Difficulty',
                               [("Easy", ), ("Normal", ), ("Hard", )],
                               default=1,
                               onchange=change_difficulty,
                               onreturn=change_difficulty)

    settings.add_option('Return to Menu', pygameMenu.events.BACK)

    # Main menu, pauses execution of the application
    menu = pygameMenu.Menu(surface,
                                bgfun=mainmenu_background,
                                enabled=True,
                                font=pygameMenu.font.FONT_NEVIS,
                                menu_alpha=90,
                                fps=FPS,
                                onclose=pygameMenu.events.CLOSE,
                                title='Main Menu',
                                title_offsety=5,
                                window_height=H_SIZE,
                                window_width=W_SIZE
                                )

    menu.add_option(settings.get_title(), settings)
    menu.add_option("Close", pygameMenu.events.CLOSE)
    menu.add_option('Exit', pygameMenu.events.EXIT)  # Add exit function

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:

        # Tick clock

        # Paint background
        surface.fill(COLOR_BACKGROUND)

        # Application events
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.enable()

        # Execute main from principal menu if is enabled
        menu.mainloop(events, disable_loop=test)

        # Flip surface
        pygame.display.flip()

        # At first loop returns
        if test:
            break


if __name__ == '__main__':
    main()
