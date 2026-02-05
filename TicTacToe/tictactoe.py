import pygame
import numpy as np
import random

import Settings.settings as s
import Settings.colors as fc
from Settings.icons import draw_icon
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def tictactoe_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()

    # 3x3 Grid in 32x32 Pixel-Flaeche (640x640 bei PIXEL_WIDTH=20)
    cell = 10 * s.PIXEL_WIDTH          # 200px
    grid_size = 3 * cell               # 600px
    ox = (s.SCREEN_WIDTH - grid_size) // 2   # 20px
    oy = (s.SCREEN_HEIGHT - grid_size) // 2  # 20px
    thickness = s.PIXEL_WIDTH

    # --------- Colors / Effects ----------
    X_COLOR = fc.RED
    O_COLOR = fc.TETRIS_J         # nice blue
    WIN_BLINK = fc.GREEN          # winner blink
    DRAW_BLINK = fc.RED           # draw blink
    GRID_COLOR = fc.DARK_GRAY

    # Explosion color = loser color (so you "see" who lost)
    LOSE_COLOR_IF_X_WINS = O_COLOR  # O loses -> blue boom
    LOSE_COLOR_IF_O_WINS = X_COLOR  # X loses -> red boom

    # --- Pixel-Art Marks (sehen auf Matrix sauber aus) ---
    X_10 = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    ])

    O_10 = np.array([
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    ])

    MARK_COLORS_X = {0: fc.BLACK, 1: X_COLOR}
    MARK_COLORS_O = {0: fc.BLACK, 1: O_COLOR}

    # ---------- FX state (persist between frames) ----------
    confetti = []  # list of dicts: {x,y,vx,vy,life,color}
    boom = []      # list of dicts: {x,y,vx,vy,life,color}
    fx_winner = None
    fx_started = False

    def reset_fx():
        nonlocal confetti, boom, fx_winner, fx_started
        confetti = []
        boom = []
        fx_winner = None
        fx_started = False

    def spawn_confetti():
        # confetti from top, falling down (front overlay)
        nonlocal confetti
        colors = [fc.WHITE, fc.YELLOW, fc.GREEN, X_COLOR, O_COLOR]
        for _ in range(120):
            x = random.randint(0, s.SCREEN_WIDTH // s.PIXEL_WIDTH - 1) * s.PIXEL_WIDTH
            y = random.randint(-20, 0) * s.PIXEL_WIDTH
            vx = random.choice([-1, 0, 1]) * s.PIXEL_WIDTH
            vy = random.randint(1, 3) * s.PIXEL_WIDTH
            life = random.randint(20, 45)
            col = random.choice(colors)
            confetti.append({"x": x, "y": y, "vx": vx, "vy": vy, "life": life, "c": col})

    def spawn_boom(color):
        # explosion from center outward (front overlay)
        nonlocal boom
        cx = s.SCREEN_WIDTH // 2
        cy = s.SCREEN_HEIGHT // 2
        for _ in range(160):
            # direction
            dx = random.randint(-6, 6)
            dy = random.randint(-6, 6)
            if dx == 0 and dy == 0:
                dx = 1
            # speed in "matrix pixels"
            vx = dx * s.PIXEL_WIDTH
            vy = dy * s.PIXEL_WIDTH
            life = random.randint(12, 22)
            boom.append({"x": cx, "y": cy, "vx": vx, "vy": vy, "life": life, "c": color})

    def update_particles():
        nonlocal confetti, boom
        # confetti
        for p in confetti:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        confetti = [p for p in confetti if p["life"] > 0 and p["y"] < s.SCREEN_HEIGHT + 5 * s.PIXEL_WIDTH]

        # boom
        for p in boom:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            # slight slowdown
            p["vx"] = int(p["vx"] * 0.85)
            p["vy"] = int(p["vy"] * 0.85)
            p["life"] -= 1
        boom = [p for p in boom if p["life"] > 0]

    def draw_particles():
        # Draw as matrix-sized pixels so it looks crisp on right preview
        for p in confetti:
            pygame.draw.rect(screen, p["c"], (p["x"], p["y"], s.PIXEL_WIDTH, s.PIXEL_WIDTH))
        for p in boom:
            pygame.draw.rect(screen, p["c"], (p["x"], p["y"], s.PIXEL_WIDTH, s.PIXEL_WIDTH))

    def reset():
        reset_fx()
        board = [[None for _ in range(3)] for _ in range(3)]  # None, "X", "O"
        sel_r, sel_c = 0, 0
        current = "X"
        game_over = False
        winner = None
        win_cells = []
        return board, sel_r, sel_c, current, game_over, winner, win_cells

    def cell_rect(r, c):
        return pygame.Rect(ox + c * cell, oy + r * cell, cell, cell)

    def draw_x(rect):
        px = rect.x + (rect.w - 10 * s.PIXEL_WIDTH) // 2
        py = rect.y + (rect.h - 10 * s.PIXEL_WIDTH) // 2
        draw_icon(screen, px, py, X_10, MARK_COLORS_X, s.PIXEL_WIDTH)

    def draw_o(rect):
        px = rect.x + (rect.w - 10 * s.PIXEL_WIDTH) // 2
        py = rect.y + (rect.h - 10 * s.PIXEL_WIDTH) // 2
        draw_icon(screen, px, py, O_10, MARK_COLORS_O, s.PIXEL_WIDTH)

    def check_winner(board):
        # rows
        for r in range(3):
            if board[r][0] and board[r][0] == board[r][1] == board[r][2]:
                return board[r][0], [(r, 0), (r, 1), (r, 2)]
        # cols
        for c in range(3):
            if board[0][c] and board[0][c] == board[1][c] == board[2][c]:
                return board[0][c], [(0, c), (1, c), (2, c)]
        # diags
        if board[0][0] and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0], [(0, 0), (1, 1), (2, 2)]
        if board[0][2] and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2], [(0, 2), (1, 1), (2, 0)]
        # draw?
        if all(board[r][c] is not None for r in range(3) for c in range(3)):
            return "DRAW", []
        return None, []

    while True:
        board, sel_r, sel_c, current, game_over, winner, win_cells = reset()
        run = True

        while run:
            events = pygame.event.get()
            input_handler.process_events(events)

            # exit/back -> zurück ins Menü
            if input_handler.is_pressed(inputs.BACK):
                return

            if not game_over:
                # navigation
                if input_handler.is_pressed(inputs.LEFT):
                    sel_c = max(0, sel_c - 1)
                if input_handler.is_pressed(inputs.RIGHT):
                    sel_c = min(2, sel_c + 1)
                if input_handler.is_pressed(inputs.UP):
                    sel_r = max(0, sel_r - 1)
                if input_handler.is_pressed(inputs.DOWN):
                    sel_r = min(2, sel_r + 1)

                # place mark
                if input_handler.is_pressed(inputs.CONFIRM):
                    if board[sel_r][sel_c] is None:
                        board[sel_r][sel_c] = current
                        w, cells = check_winner(board)
                        if w:
                            winner = w
                            win_cells = cells
                            game_over = True
                            fx_winner = winner
                            fx_started = False  # start next render
                        else:
                            current = "O" if current == "X" else "X"
            else:
                # game over: CONFIRM = restart
                if input_handler.is_pressed(inputs.CONFIRM):
                    run = False  # restart outer loop

            # ---------------- RENDER ----------------
            screen.fill(fc.BLACK)

            # Winner blink background (green), draw blink background (red)
            if game_over:
                blink = (pygame.time.get_ticks() // 250) % 2 == 0
                if fx_winner in ("X", "O"):
                    if blink:
                        screen.fill(WIN_BLINK)
                elif fx_winner == "DRAW":
                    if blink:
                        screen.fill(DRAW_BLINK)

            # grid + marks
            for r in range(3):
                for c in range(3):
                    rect = cell_rect(r, c)

                    # subtle highlight winning cells
                    if game_over and fx_winner in ("X", "O") and (r, c) in win_cells:
                        pygame.draw.rect(screen, fc.BLACK, rect)

                    pygame.draw.rect(screen, GRID_COLOR, rect, thickness)

                    mark = board[r][c]
                    if mark == "X":
                        draw_x(rect)
                    elif mark == "O":
                        draw_o(rect)

            # selection cursor (only while playing)
            if not game_over:
                sel_rect = cell_rect(sel_r, sel_c)
                pygame.draw.rect(screen, fc.WHITE, sel_rect, thickness)

            # ---------------- FRONT OVERLAY FX (on top!) ----------------
            if game_over:
                # start fx once
                if not fx_started:
                    fx_started = True
                    if fx_winner in ("X", "O"):
                        # Confetti for winner + BOOM for loser
                        spawn_confetti()
                        if fx_winner == "X":
                            spawn_boom(LOSE_COLOR_IF_X_WINS)
                        else:
                            spawn_boom(LOSE_COLOR_IF_O_WINS)
                    elif fx_winner == "DRAW":
                        # draw: more chaotic boom (white + red mix)
                        for _ in range(2):
                            spawn_boom(fc.WHITE)
                        spawn_boom(fc.RED)

                update_particles()
                draw_particles()

                # small end border blink
                blink2 = (pygame.time.get_ticks() // 300) % 2 == 0
                if blink2:
                    pygame.draw.rect(
                        screen,
                        fc.WHITE,
                        pygame.Rect(ox, oy, grid_size, grid_size),
                        thickness
                    )

            # display update (matrix or preview)
            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                pygame.display.update()

            clock.tick(30)
