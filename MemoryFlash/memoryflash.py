import random
import pygame

import Settings.settings as s
import Settings.colors as fc
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def memory_flash_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()
    PW = s.PIXEL_WIDTH

    # --- Layout (3x3 in 32x32 Fläche -> wie TicTacToe: 10 Matrix-Pixel pro Feld) ---
    grid_n = s.MF_GRID_N          # 3
    cell = s.MF_CELL             # 10 * PIXEL_WIDTH
    grid_size = grid_n * cell
    ox = (s.SCREEN_WIDTH - grid_size) // 2
    oy = (s.SCREEN_HEIGHT - grid_size) // 2
    thickness = PW

    # -----------------------
    # Score (oben links) – ohne draw_score()
    # -----------------------
    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    FONT_3x5 = {
        "0": [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]],
        "1": [[0, 1, 0], [1, 1, 0], [0, 1, 0], [0, 1, 0], [1, 1, 1]],
        "2": [[1, 1, 1], [0, 0, 1], [1, 1, 1], [1, 0, 0], [1, 1, 1]],
        "3": [[1, 1, 1], [0, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
        "4": [[1, 0, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [0, 0, 1]],
        "5": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
        "6": [[1, 1, 1], [1, 0, 0], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
        "7": [[1, 1, 1], [0, 0, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
        "8": [[1, 1, 1], [1, 0, 1], [1, 1, 1], [1, 0, 1], [1, 1, 1]],
        "9": [[1, 1, 1], [1, 0, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]],
        " ": [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    }

    def rect_from_grid(mx, my, mw=1, mh=1):
        return pygame.Rect(mx * PW, my * PW, mw * PW, mh * PW)

    def draw_char(ch: str, mx: int, my: int, color):
        glyph = FONT_3x5.get(ch, FONT_3x5[" "])
        for gy in range(5):
            for gx in range(3):
                if glyph[gy][gx]:
                    pygame.draw.rect(screen, color, rect_from_grid(mx + gx, my + gy))

    def draw_2digit(number: int, mx: int, my: int, color):
        number = clamp(int(number), 0, 99)
        tens = number // 10
        ones = number % 10
        draw_char(str(tens), mx, my, color)
        draw_char(str(ones), mx + 4, my, color)  # 3 + 1 spacing

    # -----------------------
    # Grid helpers
    # -----------------------
    def cell_rect(r, c):
        return pygame.Rect(ox + c * cell, oy + r * cell, cell, cell)

    def idx_from_rc(r, c):
        return r * grid_n + c

    def rc_from_idx(idx):
        return idx // grid_n, idx % grid_n

    # -----------------------
    # Game state
    # -----------------------
    # sequence element: (cell_index, color_tuple)
    sequence = []
    score = 0

    cursor_r, cursor_c = 0, 0

    # phases: "SHOW", "INPUT", "FAIL"
    phase = "SHOW"
    input_pos = 0

    # show state machine
    show_step = 0
    next_switch_ms = 0
    active_idx = None
    active_color = None

    fail_until_ms = 0

    # -----------------------
    # helpers
    # -----------------------
    def add_step():
        cell_idx = random.randint(0, grid_n * grid_n - 1)
        color = random.choice(fc.MF_PALETTE)
        sequence.append((cell_idx, color))

    def reset_run():
        nonlocal sequence, score, cursor_r, cursor_c, phase, input_pos
        nonlocal show_step, next_switch_ms, active_idx, active_color
        nonlocal fail_until_ms

        sequence = []
        score = 0
        cursor_r, cursor_c = 0, 0

        add_step()

        phase = "SHOW"
        input_pos = 0

        show_step = 0
        next_switch_ms = pygame.time.get_ticks() + s.MF_START_DELAY_MS
        active_idx = None
        active_color = None

        fail_until_ms = 0

    def start_show():
        nonlocal phase, input_pos, show_step, next_switch_ms, active_idx, active_color
        phase = "SHOW"
        input_pos = 0
        show_step = 0
        active_idx = None
        active_color = None
        next_switch_ms = pygame.time.get_ticks() + s.MF_START_DELAY_MS

    def start_input():
        nonlocal phase, input_pos, active_idx, active_color
        phase = "INPUT"
        input_pos = 0
        active_idx = None
        active_color = None

    def start_fail():
        nonlocal phase, fail_until_ms, active_idx, active_color
        phase = "FAIL"
        fail_until_ms = pygame.time.get_ticks() + s.MF_FAIL_MS
        active_idx, active_color = None, None

    reset_run()

    # -----------------------
    # main loop
    # -----------------------
    while True:
        now = pygame.time.get_ticks()
        events = pygame.event.get()
        input_handler.process_events(events)

        # back to menu
        if input_handler.is_pressed(inputs.BACK):
            return

        # --------------------
        # UPDATE
        # --------------------
        if phase == "SHOW":
            if now >= next_switch_ms:
                # SHOW toggles between ON and OFF for each sequence element
                if show_step >= len(sequence) * 2:
                    start_input()
                else:
                    seq_i = show_step // 2
                    is_on = (show_step % 2 == 0)

                    if is_on:
                        active_idx, active_color = sequence[seq_i]
                        next_switch_ms = now + s.MF_FLASH_ON_MS
                    else:
                        active_idx, active_color = None, None
                        next_switch_ms = now + s.MF_FLASH_OFF_MS

                    show_step += 1

        elif phase == "INPUT":
            # move cursor
            if input_handler.is_pressed(inputs.LEFT):
                cursor_c = max(0, cursor_c - 1)
            if input_handler.is_pressed(inputs.RIGHT):
                cursor_c = min(grid_n - 1, cursor_c + 1)
            if input_handler.is_pressed(inputs.UP):
                cursor_r = max(0, cursor_r - 1)
            if input_handler.is_pressed(inputs.DOWN):
                cursor_r = min(grid_n - 1, cursor_r + 1)

            # confirm selection
            if input_handler.is_pressed(inputs.CONFIRM):
                chosen = idx_from_rc(cursor_r, cursor_c)
                expected_idx, expected_color = sequence[input_pos]

                if chosen == expected_idx:
                    # tiny feedback flash (optional)
                    active_idx, active_color = expected_idx, expected_color

                    input_pos += 1
                    if input_pos >= len(sequence):
                        score += 1
                        add_step()
                        start_show()
                else:
                    start_fail()

        elif phase == "FAIL":
            if now >= fail_until_ms:
                reset_run()

        # --------------------
        # RENDER
        # --------------------
        screen.fill(fc.MF_BG)

        # static grid
        for r in range(grid_n):
            for c in range(grid_n):
                rect = cell_rect(r, c)
                pygame.draw.rect(screen, fc.MF_CELL_BG, rect)
                pygame.draw.rect(screen, fc.MF_GRID_COLOR, rect, thickness)

        # active flash cell (SHOW phase OR tiny input feedback)
        if active_idx is not None and active_color is not None:
            ar, ac = rc_from_idx(active_idx)
            rect = cell_rect(ar, ac)
            pygame.draw.rect(screen, active_color, rect)
            pygame.draw.rect(screen, fc.MF_GRID_COLOR, rect, thickness)

        # cursor only in input phase
        if phase == "INPUT":
            cur = cell_rect(cursor_r, cursor_c)
            pygame.draw.rect(screen, fc.MF_CURSOR, cur, thickness)

        # fail overlay (score bleibt sichtbar)
        if phase == "FAIL":
            screen.fill(fc.MF_FAIL)
            pygame.draw.rect(screen, fc.WHITE, (0, s.SCREEN_HEIGHT - PW, s.SCREEN_WIDTH, PW))

        # turn indicator: SHOW = gelb, INPUT = weiß, FAIL = weiß
        ind_color = fc.MF_IND_SHOW if phase == "SHOW" else fc.MF_IND_INPUT
        if phase == "FAIL":
            ind_color = fc.WHITE
        pygame.draw.rect(screen, ind_color, (PW, s.SCREEN_HEIGHT - 2 * PW, PW, PW))

        # score oben links (00..99)
        draw_2digit(score, 1, 1, fc.WHITE)

        # output
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)