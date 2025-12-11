import os
import pygame
from pygame.locals import *
import Settings.settings as s
import Settings.colors as fc
from Settings.icons import *
from Settings.output import draw_matrix, draw_matrix_representation
from Snake.snake import snake_game

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

select_box_x = 0
select_box_y = 0

run = True
while(run):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                select_box_x = 0
            elif event.key == K_RIGHT:
                select_box_x = s.SCREEN_HALF
            elif event.key == K_UP:
                select_box_y = 0
            elif event.key == K_DOWN:
                select_box_y = s.SCREEN_HALF
            elif event.key == K_RETURN:
                # Snake (bottom-left) + Exit (bottom-right)
                if select_box_x == 0 and select_box_y == 0:
                    snake_game(screen, matrix, offset_canvas)
                elif select_box_x == s.SCREEN_HALF and select_box_y == s.SCREEN_HALF:
                    run = False

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis == 0:
                if event.value < -0.5:
                    select_box_x = 0
                elif event.value > 0.5:
                    select_box_x = s.SCREEN_HALF
            elif event.axis == 1:
                if event.value < -0.5:
                    select_box_y = 0
                elif event.value > 0.5:
                    select_box_y = s.SCREEN_HALF

        elif event.type == pygame.JOYBUTTONDOWN and event.button != 8:
            if select_box_x == 0 and select_box_y == 0:
                snake_game(screen, matrix, offset_canvas)
            elif select_box_x == s.SCREEN_HALF and select_box_y == s.SCREEN_HALF:
                run = False

    # Top-left = snake
    draw_icon_snake(screen, 0, 0)

    # Top-right = X
    draw_icon_x(screen, s.SCREEN_HALF, 0)

    # Bottom-left = X
    draw_icon_x(screen, 0, s.SCREEN_HALF)

    # Bottom-right = OFF
    draw_icon_poweroff(screen, s.SCREEN_HALF, s.SCREEN_HALF)

    # Selection
    pygame.draw.rect(screen, fc.WHITE, (select_box_x, select_box_y, s.SCREEN_HALF, s.SCREEN_HALF), s.PIXEL_WIDTH)

    if started_on_pi:
        draw_matrix(screen, matrix, offset_canvas)
    else:
        draw_matrix_representation(screen)
        pygame.display.update()

pygame.quit()
if started_on_pi:
    os.system("sudo shutdown -h now")
