import pygame
import Settings.colors as fc
import Settings.settings as s
from Settings.icons import draw_icon_poweroff
from Settings import inputs

STATE_START = "START"
STATE_EXIT = "EXIT"

def run_homescreen(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()
    run = True

    while run:
        events = pygame.event.get()
        input_handler.process_events(events)

        # BACK = Exit
        if input_handler.is_pressed(inputs.BACK):
            return STATE_EXIT

        # Wenn **irgendeine andere Taste gedrückt** → Startseite
        for action in [inputs.UP, inputs.DOWN, inputs.LEFT, inputs.RIGHT, inputs.CONFIRM, inputs.DROP, inputs.HOLD]:
            if input_handler.is_pressed(action):
                return STATE_START
        
        draw_homescreen(screen)

        if started_on_pi:
            from Settings.output import draw_matrix
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            from Settings.output import draw_matrix_representation
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)

def draw_homescreen(screen):
    # DRAW
    screen.fill(fc.BLACK)
    draw_icon_poweroff(screen, 0, 0)