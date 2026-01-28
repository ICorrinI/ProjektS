import pygame
import Settings.colors as fc
import Settings.settings as s
from Settings import inputs
import math
import time

STATE_START = "START"
STATE_EXIT = "EXIT"

def run_homescreen(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()
    run = True
    start_time = time.time()

    while run:
        events = pygame.event.get()
        input_handler.process_events(events)

        # BACK = Exit
        if input_handler.is_pressed(inputs.BACK):
            return STATE_EXIT

        # Wenn irgendeine Taste gedrückt wird → Startseite
        for action in [inputs.UP, inputs.DOWN, inputs.LEFT, inputs.RIGHT, inputs.CONFIRM, inputs.DROP, inputs.HOLD]:
            if input_handler.is_pressed(action):
                play_start_animation(screen, clock, started_on_pi)
                return STATE_START
        
        elapsed = time.time() - start_time
        draw_homescreen(screen, elapsed)

        if started_on_pi:
            from Settings.output import draw_matrix
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            from Settings.output import draw_matrix_representation
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)


def draw_homescreen(screen, elapsed):
    """
    Zeichnet den Homescreen mit pulsierendem Kreis in der Mitte.
    """
    screen.fill(fc.BLACK)

    # Zentrum immer exakt in der Mitte des Fensters
    w, h = s.SCREEN_WIDTH, s.SCREEN_HEIGHT
    center = (w // 2, h // 2)

    # Pulsierender Kreis
    base_radius = 50
    pulse = int(10 * math.sin(elapsed * 2))
    radius = base_radius + pulse

    # Glow Effekt: mehrere Kreise
    for i in range(5, 0, -1):
        alpha = int(50 / i)
        pygame.draw.circle(screen, (*fc.WHITE, alpha), center, radius + i * 8, width=2)

    # Kernkreis
    pygame.draw.circle(screen, fc.WHITE, center, radius)

    pygame.display.update()


def play_start_animation(screen, clock, started_on_pi=False):
    """
    Animierte Übergang zum Startscreen
    """
    w, h = s.SCREEN_WIDTH, s.SCREEN_HEIGHT
    center = (w // 2, h // 2)
    max_radius = 200

    for frame in range(30):  # ~1 Sekunde bei 30 FPS
        screen.fill(fc.BLACK)
        t = frame / 30
        radius = int(t * max_radius)
        alpha = int(t * 255)

        # Glow
        for i in range(5, 0, -1):
            a = max(0, alpha - i * 30)
            pygame.draw.circle(screen, (0, 255, 255, a), center, radius + i * 10, width=2)

        # Kernkreis
        pygame.draw.circle(screen, fc.WHITE, center, radius)
        pygame.display.update()
        clock.tick(30)
