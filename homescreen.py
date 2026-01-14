import pygame
import Settings.colors as fc
import Settings.settings as s
from Settings.icons import draw_icon_poweroff

STATE_START = "START"
STATE_EXIT = "EXIT"

def run_homescreen(screen, matrix, offset_canvas, started_on_pi):
    clock = pygame.time.Clock()
    selected = STATE_START

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return STATE_EXIT

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    selected = STATE_EXIT if selected == STATE_START else STATE_START

                elif event.key == pygame.K_RETURN:
                    return selected
        # ---- DRAW ----
        screen.fill(fc.BLACK)
        
        # POWER ICON
        draw_icon_poweroff(screen, 0, 0)

        if started_on_pi:
            from Settings.output import draw_matrix
            draw_matrix(screen, matrix, offset_canvas)
        else:
            from Settings.output import draw_matrix_representation
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)
