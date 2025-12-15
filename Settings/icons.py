import pygame
import numpy as np
import Settings.colors as fc
import Settings.settings as s


def draw_icon_x(screen, x_offset, y_offset):
    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, s.SCREEN_HALF))
    pygame.draw.line(
        screen, fc.GRAY,
        (x_offset + 20, y_offset + 20),
        (x_offset + s.SCREEN_HALF - 20, y_offset + s.SCREEN_HALF - 20),
        s.PIXEL_WIDTH
    )
    pygame.draw.line(
        screen, fc.GRAY,
        (x_offset + s.SCREEN_HALF - 20, y_offset + 20),
        (x_offset + 20, y_offset + s.SCREEN_HALF - 20),
        s.PIXEL_WIDTH
    )


def draw_icon_snake(screen, x_offset, y_offset):
    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, s.SCREEN_HALF))

    pygame.draw.rect(screen, fc.GREEN, (x_offset + 0,   y_offset + 200, 140, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 60,  y_offset + 160, 80,  s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 60,  y_offset + 120, 160, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 200, y_offset + 140, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 60,  y_offset + 140, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 120, y_offset + 180, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.RED, (x_offset + 200, y_offset + 200, s.PIXEL_WIDTH, s.PIXEL_WIDTH))


def draw_icon_poweroff(screen, x_offset, y_offset):
    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, s.SCREEN_HALF))

    pygame.draw.circle(
        screen,
        fc.RED,
        (x_offset + 470 - s.SCREEN_HALF, y_offset + 471 + s.DOWNWARD_PIXEL_PULL_OFFSET - s.SCREEN_HALF),
        129,
        s.PIXEL_WIDTH
    )

    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, 60))
    pygame.draw.rect(screen, fc.RED, (x_offset + 140, y_offset + 40, 40, 120))

def draw_icon_doodle_jump(screen, x_offset, y_offset):
    doodle_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    doodle_colors = {
    0: fc.BLACK,
    1: fc.YELLOW,
    2: fc.WHITE,
    3: fc.GREEN
    }
    draw_icon(screen, x_offset, y_offset, pixel_array=doodle_array, color_mapping=doodle_colors, pixel_size=s.PIXEL_WIDTH)

def draw_icon(screen, x_offset, y_offset, pixel_array, color_mapping, pixel_size):
    """
    Zeichnet ein Icon basierend auf einem 2D-Array von Zahlen und einem Farb-Mapping.

    :param screen: Pygame Surface
    :param x_offset: Start-x-Koordinate auf dem Screen
    :param y_offset: Start-y-Koordinate auf dem Screen
    :param pixel_array: 2D-Array mit Zahlen (z.B. Numpy oder Liste von Listen)
    :param color_mapping: Dict {int: (R,G,B)} für Farben
    :param pixel_size: Größe eines einzelnen Pixels auf dem Screen
    """
    height = len(pixel_array)
    width = len(pixel_array[0]) if height > 0 else 0

    # Hintergrund schwarz
    pygame.draw.rect(screen, (0, 0, 0), (x_offset, y_offset, width*pixel_size, height*pixel_size))

    # Pixel zeichnen
    for y in range(height):
        for x in range(width):
            color = color_mapping.get(pixel_array[y][x], (255, 255, 255))  # default: Weiß
            pygame.draw.rect(
                screen,
                color,
                (x_offset + x*pixel_size, y_offset + y*pixel_size, pixel_size, pixel_size)
            )
