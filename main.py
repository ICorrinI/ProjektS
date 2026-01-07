import os
import pygame
from pygame.locals import *
import Settings.settings as s
import Settings.colors as fc
from Settings.output import draw_matrix, draw_matrix_representation
from gameregistry import GAMES


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
    options.hardware_mapping = 'adafruit-hat'
    options.drop_privileges = 0

    matrix = RGBMatrix(options=options)
    offset_canvas = matrix.CreateFrameCanvas()

pygame.init()
pygame.joystick.init()

joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
if not joysticks:
    print("No gamepads detected.")

for joystick in joysticks:
    joystick.init()
    print(f"Detected Gamepad: {joystick.get_name()}")

screen = None
if started_on_pi:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH, s.SCREEN_HEIGHT))
else:
    screen = pygame.display.set_mode((s.SCREEN_WIDTH*2, s.SCREEN_HEIGHT))

pygame.display.set_caption("Startscreen")

# ---- MENU STATE ----
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

run = True
clock = pygame.time.Clock()

# ---- MAIN LOOP ----
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
                    if not game["enabled"]:
                        pass
                    elif game["run"] == "EXIT":
                        run = False
                    else:
                        game["run"](screen, matrix, offset_canvas, started_on_pi)

        # For Joystick support send KEYDOWN events if joystick is used
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

    screen.fill((0, 0, 0))

    # ---- DRAW ICONS ----
    for i, game in enumerate(get_page_items()):
        x, y = index_to_pos(i)
        game["icon"](screen, x, y)

    # ---- SELECTION ----
    sel_x, sel_y = index_to_pos(selected_index)
    pygame.draw.rect(screen,fc.WHITE,(sel_x, sel_y, s.SCREEN_HALF, s.SCREEN_HALF),s.PIXEL_WIDTH,)

    if started_on_pi:
        draw_matrix(screen, matrix, offset_canvas)
    else:
        draw_matrix_representation(screen)
        pygame.display.update()

    clock.tick(30)

pygame.quit()
if started_on_pi:
    os.system("sudo shutdown -h now")
