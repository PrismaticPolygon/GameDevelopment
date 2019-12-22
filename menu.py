import os
import pygame
import pygameMenu

COLOR_BLUE = (12, 12, 200)
COLOR_BACKGROUND = [128, 0, 128]
COLOR_WHITE = (255, 255, 255)
FPS = 60
HEIGHT = 600  # Height of window size
WIDTH = 800  # Width of window size

surface = None
#
def menu_background():
    """
    Background color of the main menu, on this function user can plot
    images, play sounds, etc.
    """

    pass

    # We probably want to draw the dim screen, same as on pause.

    # global surface
    # surface.fill((40, 0, 40))

DIFFICULTY = 1

def change_difficulty(value):

    difficulty, _ = value

    if difficulty == "Easy":

        DIFFICULTY = 0.75

    elif difficulty == "Normal":

        DIFFICULTY = 1

    elif difficulty == "Hard":

        DIFFICULTY = 1.25


def create_menu(surface):

    settings = pygameMenu.Menu(surface,
                               dopause=True,
                               font=pygameMenu.font.FONT_NEVIS,
                               menu_alpha=85,
                               menu_color=(0, 0, 0),  # Background color
                               menu_color_title=(0, 0, 0),
                               menu_height=int(HEIGHT * 0.65),
                               menu_width=600,
                               onclose=pygameMenu.events.RESET,  # If this menu closes (ESC) back to main
                               option_shadow=True,
                               rect_width=4,
                               title='Settings',
                               title_offsety=5,  # Adds 5px to title vertical position
                               window_height=HEIGHT,
                               window_width=WIDTH
                               )

    settings.add_selector('Difficulty',
                          [("Easy",), ("Normal",), ("Hard",)],
                          default=1,
                          onchange=change_difficulty,
                          onreturn=change_difficulty)

    settings.add_option('Return to Menu', pygameMenu.events.BACK)

    # Main menu, pauses execution of the application
    menu = pygameMenu.Menu(surface,
                           bgfun=lambda x: x,
                           enabled=True,
                           font=pygameMenu.font.FONT_NEVIS,
                           menu_alpha=90,
                           fps=FPS,
                           onclose=pygameMenu.events.CLOSE,
                           title='Main Menu',
                           title_offsety=5,
                           window_height=HEIGHT,
                           window_width=WIDTH
                           )

    menu.add_option(settings.get_title(), settings)
    menu.add_option("Close", pygameMenu.events.CLOSE)
    menu.add_option('Exit', pygameMenu.events.EXIT)  # Add exit function

    return menu

#
# def main():
#
#     pygame.init()
#     os.environ['SDL_VIDEO_CENTERED'] = '1'
#
#     # Create window
#     global surface
#     surface = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption('Example - Timer Clock')
#
#     settings = pygameMenu.Menu(surface,
#                                dopause=False,
#                                font=pygameMenu.font.FONT_NEVIS,
#                                menu_alpha=85,
#                                menu_color=(0, 0, 0),  # Background color
#                                  menu_color_title=(0, 0, 0),
#                                menu_height=int(HEIGHT * 0.65),
#                                menu_width=600,
#                                onclose=pygameMenu.events.RESET,  # If this menu closes (ESC) back to main
#                                  option_shadow=True,
#                                rect_width=4,
#                                title='Settings',
#                                title_offsety=5,  # Adds 5px to title vertical position
#                                  window_height=HEIGHT,
#                                window_width=WIDTH
#                                )
#
#     settings.add_selector('Difficulty',
#                                [("Easy", ), ("Normal", ), ("Hard", )],
#                                default=1,
#                                onchange=change_difficulty,
#                                onreturn=change_difficulty)
#
#     settings.add_option('Return to Menu', pygameMenu.events.BACK)
#
#     # Main menu, pauses execution of the application
#     menu = pygameMenu.Menu(surface,
#                            bgfun=menu_background,
#                            enabled=True,
#                            font=pygameMenu.font.FONT_NEVIS,
#                            menu_alpha=90,
#                            fps=FPS,
#                            onclose=pygameMenu.events.CLOSE,
#                            title='Main Menu',
#                            title_offsety=5,
#                            window_height=HEIGHT,
#                            window_width=WIDTH
#                            )
#
#     menu.add_option(settings.get_title(), settings)
#     menu.add_option("Close", pygameMenu.events.CLOSE)
#     menu.add_option('Exit', pygameMenu.events.EXIT)  # Add exit function
#
#     while True:
#
#         # Paint background
#         surface.fill(COLOR_BACKGROUND)
#
#         # Application events
#         events = pygame.event.get()
#         for event in events:
#             if event.type == pygame.QUIT:
#                 exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     menu.enable()
#
#         # Execute main from principal menu if is enabled
#         menu.mainloop(events)
#
#         # Flip surface
#         pygame.display.flip()
#
# if __name__ == '__main__':
#
#     main()
