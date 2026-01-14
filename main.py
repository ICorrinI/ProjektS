import os
import pygame
from pygame.locals import *

import Settings.settings as s
import Settings.colors as fc
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
    import threading
    from evdev import InputDevice, categorize, ecodes, list_devices
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "adafruit-hat"
    options.drop_privileges = 0

    matrix = RGBMatrix(options=options)
    offset_canvas = matrix.CreateFrameCanvas()

    KEY_MAP = {
    ecodes.KEY_LEFT: pygame.K_LEFT,
    ecodes.KEY_RIGHT: pygame.K_RIGHT,
    ecodes.KEY_UP: pygame.K_UP,
    ecodes.KEY_DOWN: pygame.K_DOWN,
    ecodes.KEY_ENTER: pygame.K_RETURN,
    }

# -------------------------------------------------
# PYGAME INIT
# -------------------------------------------------
pygame.init()
pygame.joystick.init()


# -------------------------------------------------
# PY INPUT HANDLING
# -------------------------------------------------
def _find_keyboard():
    for path in list_devices():
        dev = InputDevice(path)
        if "keyboard" in dev.name.lower():
            return dev
    return None

def start_evdev_keyboard():
    keyboard = _find_keyboard()
    if not keyboard:
        print("No keyboard found via evdev")
        return

    print(f"evdev keyboard: {keyboard.name}")

    try:
        keyboard.grab()
        print("Keyboard grabbed successfully")
    except OSError as e:
        print(f"Failed to grab keyboard: {e}")
        return

    def _reader():
        for event in keyboard.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)
                if key.keystate == key.key_down:
                    mapped = KEY_MAP.get(key.scancode)
                    if mapped:
                        pygame.event.post(
                            pygame.event.Event(pygame.KEYDOWN, key=mapped)
                        )

    threading.Thread(target=_reader, daemon=True).start()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

if started_on_pi:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH * 2, s.SCREEN_HEIGHT))

pygame.display.set_caption("Pixel Arcade")

if started_on_pi:
    start_evdev_keyboard()
# -------------------------------------------------
# RUN HOMESCREEN (BLOCKING)
# -------------------------------------------------
result = run_homescreen(screen, matrix, offset_canvas, started_on_pi)

if result == "EXIT":
    pygame.quit()
    if started_on_pi:
        os.system("sudo shutdown -h now")
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
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if selected_index % 2 == 0:
                    if current_page > 0:
                        current_page -= 1
                else:
                    selected_index -= 1

            elif event.key == K_RIGHT:
                if selected_index % 2 == 1:
                    if current_page < max_page():
                        current_page += 1
                else:
                    selected_index += 1

            elif event.key == K_UP and selected_index >= 2:
                selected_index -= 2

            elif event.key == K_DOWN and selected_index <= 1:
                selected_index += 2

            elif event.key == K_RETURN:
                page_items = get_page_items()
                if selected_index < len(page_items):
                    game = page_items[selected_index]
                    if game["enabled"]:
                        if game["run"] == "EXIT":
                            run = False
                        else:
                            game["run"](screen, matrix, offset_canvas, started_on_pi)

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value < -0.5:
                    pygame.event.post(pygame.event.Event(KEYDOWN, key=K_LEFT))
                elif event.value > 0.5:
                    pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RIGHT))
            elif event.axis == 1:
                if event.value < -0.5:
                    pygame.event.post(pygame.event.Event(KEYDOWN, key=K_UP))
                elif event.value > 0.5:
                    pygame.event.post(pygame.event.Event(KEYDOWN, key=K_DOWN))

        elif event.type == JOYBUTTONDOWN and event.button != 8:
            pygame.event.post(pygame.event.Event(KEYDOWN, key=K_RETURN))

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
if started_on_pi:
    os.system("sudo shutdown -h now")
