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

def draw_icon_dino(screen, x_offset, y_offset):
    icon_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    icon_colors = {
        0: fc.BLACK,
        1: fc.WHITE,
    }

    

    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

def draw_game_dino(screen, x_offset, y_offset):
    dino_array = np.array([
        [0, 0, 0, 1, 0],
        [0, 0, 1, 1, 1],
        [1, 1, 1, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 1, 0, 0],
    ])

    dino_colors = {
        0: fc.BLACK,
        1: fc.WHITE
    }

    draw_icon(
        screen,
        x_offset,
        y_offset,
        pixel_array=dino_array,
        color_mapping=dino_colors,
        pixel_size=s.PIXEL_WIDTH
    )


def draw_icon_tetris(screen, x_offset, y_offset):
    icon_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 3, 4, 0, 5, 5, 3, 3, 3, 3, 0, 1, 0, 0],
    [0, 0, 1, 3, 4, 4, 6, 5, 5, 2, 2, 2, 0, 1, 0, 0],
    [0, 0, 1, 3, 7, 7, 6, 8, 8, 6, 2, 0, 0, 1, 0, 0],
    [0, 0, 1, 7, 7, 6, 6, 8, 8, 6, 6, 6, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    icon_colors = {
        0: fc.TETRIS_BG,
        1: fc.TETRIS_BORDER,

        2: fc.TETRIS_I,
        3: fc.TETRIS_T,
        4: fc.TETRIS_L,
        5: fc.TETRIS_Z,
        6: fc.TETRIS_J,
        7: fc.TETRIS_S,
        8: fc.TETRIS_O,
    }

    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

def draw_icon_mario(screen, x_offset, y_offset):
    icon_array = np.array([
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 3, 3, 4, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 3, 2, 3, 3, 4, 3, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 2, 3, 2, 2, 3, 3, 4, 3, 3, 3, 0, 0],
    [0, 0, 0, 0, 2, 3, 3, 3, 3, 4, 4, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 5, 1, 1, 5, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 5, 1, 1, 5, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 5, 5, 5, 5, 1, 1, 1, 1, 0, 0],
    [0, 0, 3, 3, 1, 5, 6, 5, 5, 6, 5, 1, 3, 3, 0, 0],
    [0, 0, 3, 3, 3, 5, 5, 5, 5, 5, 5, 3, 3, 3, 0, 0],
    [0, 0, 3, 3, 5, 5, 5, 5, 5, 5, 5, 5, 3, 3, 0, 0],
    [0, 0, 0, 0, 5, 5, 5, 0, 0, 5, 5, 5, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
    ])

    icon_colors = {
        0: (0, 0, 0),
        1: (255, 0, 0),
        2: (128, 64, 0),
        3: (255, 201, 14),
        4: (64, 0, 0),
        5: (63, 72, 204),
        6: (255, 242, 0),
    }
    
    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

def draw_icon_mario_mini(screen, x_offset, y_offset):
    icon_array = np.array([
        [1, 1],  # Rot (Mütze)
        [2, 2],  # Haut (Gesicht)
        [3, 3],  # Blau (Latzhose)
    ])

    icon_colors = {
        0: (0, 0, 0),          # Hintergrund
        1: (255, 0, 0),        # Rot
        2: (255, 201, 14),    # Hautfarbe
        3: (0, 0, 255),        # Blau
    }


    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

def draw_icon_tictactoe(screen, x_offset, y_offset):
    icon_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    icon_colors = {
        0: (0, 0, 0),
        1: (255, 255, 255),
        2: (0, 162, 232),
        3: (237, 28, 36),
    }
    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)


def draw_icon_reaction_runner(screen, x_offset, y_offset):
    # 16x16 Icon: 3 lanes + kleines "player" + obstacle
    icon_array = np.array([
        [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
        [0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,3,3,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,3,3,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,0,0,1,0,0,0,1,0,0,2],
        [2,0,0,0,1,0,4,4,4,4,0,0,1,0,0,2],
        [2,0,0,0,1,0,4,4,4,4,0,0,1,0,0,2],
        [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ])

    icon_colors = {
        0: fc.BLACK,
        1: fc.GRAY,      # lane lines
        2: fc.DARK_GRAY, # road border
        3: fc.RED,       # obstacle
        4: fc.YELLOW,    # player
    }

    draw_icon(screen, x_offset, y_offset, icon_array, icon_colors, s.PIXEL_WIDTH)
    #
def draw_icon_reaction_runner(screen, x_offset, y_offset):

    icon_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 2, 2, 2, 1, 2, 2, 2, 1, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 2, 1, 2, 2, 2, 1, 0, 0, 0],
    [0, 0, 0, 1, 2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 3, 3, 3, 1, 1, 1, 1, 3, 3, 3, 1, 1, 1, 0],
    [1, 3, 3, 0, 3, 3, 1, 1, 3, 3, 0, 3, 3, 1, 1, 0],
    [0, 0, 3, 3, 3, 0, 0, 0, 0, 3, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ])

    icon_colors = {
        0: (0, 0, 0),
        1: (255, 242, 0),
        2: (0, 162, 232),
        3: (127, 127, 127),
    }

    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

def draw_icon_stack(screen, x_offset, y_offset):
    icon_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0],
    [0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0],
    ])

    icon_colors = {
        0: (0, 0, 0),
        1: (0, 162, 232),
        2: (255, 242, 0),
        3: (255, 127, 39),
        4: (163, 73, 164),
        5: (34, 177, 76),
        6: (237, 28, 36),
    }

    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

def draw_icon_memory_flash(screen, x_offset, y_offset):
    icon_array = np.array([
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0, 1, 1],
    [0, 0, 3, 4, 5, 1, 1, 6, 7, 8, 1, 1, 4, 3, 3, 1],
    [0, 0, 4, 4, 4, 1, 1, 9, 7, 7, 1, 1, 4, 4, 4, 1],
    [0, 0, 10, 4, 10, 1, 1, 11, 7, 11, 1, 1, 12, 4, 12, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 5, 4, 3, 0, 1, 13, 14, 13, 1, 1, 15, 4, 3, 1],
    [0, 0, 4, 12, 4, 1, 1, 14, 16, 17, 1, 1, 4, 10, 4, 1],
    [0, 0, 10, 4, 18, 0, 0, 14, 14, 19, 0, 0, 10, 4, 10, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 20, 21, 22, 0, 0, 3, 4, 3, 0, 0, 3, 4, 3, 1],
    [0, 0, 21, 23, 21, 0, 0, 4, 4, 4, 0, 0, 4, 18, 4, 1],
    [0, 0, 23, 21, 23, 0, 0, 10, 4, 10, 0, 0, 10, 4, 10, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    ])

    icon_colors = {
        0: (0, 0, 0),
        1: (1, 1, 1),
        2: (20, 20, 20),
        3: (122, 122, 122),
        4: (127, 127, 127),
        5: (121, 121, 121),
        6: (229, 65, 241),
        7: (234, 63, 247),
        8: (229, 66, 241),
        9: (235, 63, 247),
        10: (126, 126, 126),
        11: (233, 64, 245),
        12: (119, 119, 119),
        13: (0, 157, 225),
        14: (0, 162, 232),
        15: (118, 118, 118),
        16: (0, 163, 232),
        17: (0, 162, 233),
        18: (125, 125, 125),
        19: (0, 160, 229),
        20: (180, 180, 180),
        21: (195, 195, 195),
        22: (182, 182, 182),
        23: (191, 191, 191),
    }

    draw_icon(screen, x_offset, y_offset,pixel_array=icon_array,color_mapping=icon_colors,pixel_size=s.PIXEL_WIDTH)

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


