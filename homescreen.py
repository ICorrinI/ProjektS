import pygame 
import Settings.colors as fc
import Settings.settings as s
from Settings import inputs
import time
import numpy as np

STATE_START = "START"
STATE_EXIT = "EXIT"

FADE_SPEED = 10  # Geschwindigkeit des Fades

def run_homescreen(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()
    current_state = 0  # 0=state1, 1=state2, 2=state3
    fade_values = [0, 0, 0]  # Fade pro State

    while True:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return STATE_EXIT

        # Start bei irgendeiner Taste
        for action in [inputs.UP, inputs.DOWN, inputs.LEFT, inputs.RIGHT,
                       inputs.CONFIRM, inputs.DROP, inputs.HOLD]:
            if input_handler.is_pressed(action):
                play_start_animation(screen, clock, started_on_pi)
                return STATE_START

        # Fade für aktuellen State hochzählen
        fade_values[current_state] = min(255, fade_values[current_state] + FADE_SPEED)

        # Zeichnen
        if current_state == 0:
            draw_state1(screen, fade_values[current_state])
        elif current_state == 1:
            draw_state2(screen, fade_values[current_state])
        elif current_state == 2:
            draw_state3(screen, fade_values[current_state])

        if started_on_pi:
            from Settings.output import draw_matrix
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            from Settings.output import draw_matrix_representation
            draw_matrix_representation(screen)
            pygame.display.update()

        # State wechseln
        if fade_values[current_state] >= 255 and current_state < 2:
            current_state += 1

        clock.tick(30)

def play_start_animation(screen, clock, started_on_pi=False):
    pass

# ---------- STATES ----------

# 32x32 Array für PLAY in Tetris-Farben
draw_state1_array = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 3, 0, 0, 0, 0, 0, 4, 4, 4, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 3, 0, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 4, 0, 0, 0, 4, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

def split_array_into_custom_thirds(array):
    h = len(array)
    third = h // 3
    top = array[:third, :]
    middle = array[third:2*third+2, :]
    bottom = array[2*third+2:, :]
    return top, middle, bottom

state1_array, state2_array, state3_array = split_array_into_custom_thirds(draw_state1_array)

def draw_state1(screen, fade):
    draw_icon_colors(screen, state1_array, fade, y_offset=0)

def draw_state2(screen, fade):
    y_offset = len(state1_array) * s.PIXEL_WIDTH
    draw_icon_colors(screen, state2_array, fade, y_offset=y_offset)

def draw_state3(screen, fade):
    y_offset = (len(state1_array) + len(state2_array)) * s.PIXEL_WIDTH
    draw_icon_colors(screen, state3_array, fade, y_offset=y_offset)

# ---------- DRAW HELPER ----------

COLOR_MAP = {
    0: fc.BLACK,
    1: fc.WHITE,    # Weiß kann weiterhin Faden
    2: fc.TETRIS_Z, # P rot
    3: fc.TETRIS_T, # L lila
    4: fc.TETRIS_O, # A orange
    5: fc.TETRIS_I, # Y cyan
}

def fade_color(color, fade):
    """Faded eine Farbe mit 0=schwarz bis 255=voll"""
    r, g, b = color
    r = r * fade // 255
    g = g * fade // 255
    b = b * fade // 255
    return (r, g, b)

def draw_icon_colors(screen, pixel_array, fade=255, y_offset=0):
    height = len(pixel_array)
    width = len(pixel_array[0])

    # Hintergrund schwarz
    pygame.draw.rect(
        screen,
        fc.BLACK,
        (0, y_offset, width * s.PIXEL_WIDTH, height * s.PIXEL_WIDTH)
    )

    for y in range(height):
        for x in range(width):
            val = pixel_array[y][x]
            if val != 0:
                color = COLOR_MAP[val]
                color = fade_color(color, fade)
                pygame.draw.rect(
                    screen,
                    color,
                    (x * s.PIXEL_WIDTH,
                     y_offset + y * s.PIXEL_WIDTH,
                     s.PIXEL_WIDTH,
                     s.PIXEL_WIDTH)
                )
