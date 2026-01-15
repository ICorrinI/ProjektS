import os
import pygame
from pygame.locals import *

import Settings.settings as s
import Settings.colors as fc
from Settings import inputs
from Settings.output import draw_matrix, draw_matrix_representation
from gameregistry import GAMES
from homescreen import run_homescreen

# -------------------------------------------------
# PI MATRIX CHECK
# -------------------------------------------------
started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
    print("Library rgbmatrix imported successfully!")
except ImportError:
    started_on_pi = False
    print("Library rgbmatrix import failed!")

os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"

matrix = None
offset_canvas = None

if started_on_pi:
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "adafruit-hat"
    options.drop_privileges = 0

    matrix = RGBMatrix(options=options)
    offset_canvas = matrix.CreateFrameCanvas()

# -------------------------------------------------
# PYGAME INIT
# -------------------------------------------------
pygame.init()
pygame.joystick.init()

if started_on_pi:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH * 2, s.SCREEN_HEIGHT))

pygame.display.set_caption("Pixel Arcade")

# -------------------------------------------------
# INPUT HANDLER INIT
# -------------------------------------------------
input_handler = inputs.InputHandler(started_on_pi=started_on_pi)

# -------------------------------------------------
# RUN HOMESCREEN (BLOCKING)
# -------------------------------------------------
result = run_homescreen(screen, matrix, offset_canvas, started_on_pi, input_handler)

if result == "EXIT":
    pygame.quit()
    #if started_on_pi:
        #os.system("sudo shutdown -h now")
    exit()

# -------------------------------------------------
# MENU STATE
# -------------------------------------------------
ITEMS_PER_PAGE = 4
current_page = 0
selected_index = 0


def get_page_items():
    start = current_page * ITEMS_PER_PAGE
    return GAMES[start:start + ITEMS_PER_PAGE]


def max_page():
    return (len(GAMES) - 1) // ITEMS_PER_PAGE


def index_to_pos(index):
    x = 0 if index % 2 == 0 else s.SCREEN_HALF
    y = 0 if index < 2 else s.SCREEN_HALF
    return x, y


clock = pygame.time.Clock()
run = True

# -------------------------------------------------
# MAIN MENU LOOP
# -------------------------------------------------
while run:
    events = pygame.event.get()
    input_handler.process_events(events)

    # QUIT
    if any(event.type == QUIT for event in events):
        run = False

    # NAVIGATION
    if input_handler.is_pressed(inputs.LEFT):
        if selected_index % 2 == 0:
            if current_page > 0:
                current_page -= 1
        else:
            selected_index -= 1

    if input_handler.is_pressed(inputs.RIGHT):
        if selected_index % 2 == 1:
            if current_page < max_page():
                current_page += 1
        else:
            selected_index += 1

    if input_handler.is_pressed(inputs.UP) and selected_index >= 2:
        selected_index -= 2

    if input_handler.is_pressed(inputs.DOWN) and selected_index <= 1:
        selected_index += 2

    # CONFIRM / ENTER
    if input_handler.is_pressed(inputs.CONFIRM):
        page_items = get_page_items()
        if selected_index < len(page_items):
            game = page_items[selected_index]
            if game["enabled"]:
                if game["run"] == "EXIT":
                    run = False
                else:
                    # Spiele sollten InputHandler als Argument bekommen
                    game["run"](screen, matrix, offset_canvas, started_on_pi, input_handler)

    # -------------------------------------------------
    # DRAW MENU
    # -------------------------------------------------
    screen.fill(fc.BLACK)

    for i, game in enumerate(get_page_items()):
        x, y = index_to_pos(i)
        game["icon"](screen, x, y)

    sel_x, sel_y = index_to_pos(selected_index)
    pygame.draw.rect(
        screen,
        fc.WHITE,
        (sel_x, sel_y, s.SCREEN_HALF, s.SCREEN_HALF),
        s.PIXEL_WIDTH,
    )

    if started_on_pi:
        draw_matrix(screen, matrix, offset_canvas)
    else:
        draw_matrix_representation(screen)
        pygame.display.update()

    clock.tick(30)

# -------------------------------------------------
# CLEAN EXIT
# -------------------------------------------------
pygame.quit()
#if started_on_pi:
#    os.system("sudo shutdown -h now")
