import pygame
import numpy as np
import random

import Settings.settings as s
import Settings.colors as fc
from Settings.icons import draw_icon
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def tictactoe_game(screen, matrix, offset_canvas, started_on_pi, input_handler):
    clock = pygame.time.Clock()

    cell = s.TTT_CELL_SIZE
    grid_size = cell * 3
    ox = (s.SCREEN_WIDTH - grid_size) // 2
    oy = (s.SCREEN_HEIGHT - grid_size) // 2
    thickness = s.PIXEL_WIDTH

    # --- FX state ---
    confetti = []
    boom = []
    fx_started = False
    fx_winner = None

    def reset_fx():
        nonlocal confetti, boom, fx_started, fx_winner
        confetti = []
        boom = []
        fx_started = False
        fx_winner = None

    def spawn_confetti():
        for _ in range(s.TTT_CONFETTI_COUNT):
            confetti.append({
                "x": random.randrange(0, s.SCREEN_WIDTH, s.PIXEL_WIDTH),
                "y": random.randrange(-200, 0, s.PIXEL_WIDTH),
                "vx": random.choice([-1, 0, 1]) * s.PIXEL_WIDTH,
                "vy": random.randint(1, 3) * s.PIXEL_WIDTH,
                "life": random.randint(20, 40),
                "c": random.choice(fc.TTT_CONFETTI_COLORS)
            })

    def spawn_boom(color):
        cx, cy = s.SCREEN_WIDTH // 2, s.SCREEN_HEIGHT // 2
        for _ in range(s.TTT_BOOM_COUNT):
            boom.append({
                "x": cx,
                "y": cy,
                "vx": random.randint(-6, 6) * s.PIXEL_WIDTH,
                "vy": random.randint(-6, 6) * s.PIXEL_WIDTH,
                "life": random.randint(12, 20),
                "c": color
            })

    def update_particles():
        for p in confetti:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1
        for p in boom:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vx"] = int(p["vx"] * 0.85)
            p["vy"] = int(p["vy"] * 0.85)
            p["life"] -= 1

    def draw_particles():
        for p in confetti + boom:
            if p["life"] > 0:
                pygame.draw.rect(
                    screen, p["c"],
                    (p["x"], p["y"], s.PIXEL_WIDTH, s.PIXEL_WIDTH)
                )

    def reset_game():
        reset_fx()
        return [[None]*3 for _ in range(3)], 0, 0, "X", False, None, []

    def cell_rect(r, c):
        return pygame.Rect(ox + c*cell, oy + r*cell, cell, cell)

    def draw_mark(mark, rect):
        px = rect.x + (rect.w - s.TTT_MARK_SIZE) // 2
        py = rect.y + (rect.h - s.TTT_MARK_SIZE) // 2
        if mark == "X":
            draw_icon(screen, px, py, s.TTT_X_ICON, fc.TTT_X_COLORS, s.PIXEL_WIDTH)
        else:
            draw_icon(screen, px, py, s.TTT_O_ICON, fc.TTT_O_COLORS, s.PIXEL_WIDTH)

    def check_winner(b):
        for i in range(3):
            if b[i][0] and b[i][0] == b[i][1] == b[i][2]:
                return b[i][0], [(i,0),(i,1),(i,2)]
            if b[0][i] and b[0][i] == b[1][i] == b[2][i]:
                return b[0][i], [(0,i),(1,i),(2,i)]
        if b[0][0] and b[0][0] == b[1][1] == b[2][2]:
            return b[0][0], [(0,0),(1,1),(2,2)]
        if b[0][2] and b[0][2] == b[1][1] == b[2][0]:
            return b[0][2], [(0,2),(1,1),(2,0)]
        if all(b[r][c] for r in range(3) for c in range(3)):
            return "DRAW", []
        return None, []

    board, sel_r, sel_c, current, game_over, winner, win_cells = reset_game()

    while True:
        input_handler.process_events(pygame.event.get())

        if input_handler.is_pressed(inputs.BACK):
            return

        if not game_over:
            if input_handler.is_pressed(inputs.LEFT):  sel_c = max(0, sel_c-1)
            if input_handler.is_pressed(inputs.RIGHT): sel_c = min(2, sel_c+1)
            if input_handler.is_pressed(inputs.UP):    sel_r = max(0, sel_r-1)
            if input_handler.is_pressed(inputs.DOWN):  sel_r = min(2, sel_r+1)

            if input_handler.is_pressed(inputs.CONFIRM):
                if board[sel_r][sel_c] is None:
                    board[sel_r][sel_c] = current
                    w, cells = check_winner(board)
                    if w:
                        winner, win_cells, game_over = w, cells, True
                        fx_winner = w
                    else:
                        current = "O" if current == "X" else "X"
        else:
            if input_handler.is_pressed(inputs.CONFIRM):
                board, sel_r, sel_c, current, game_over, winner, win_cells = reset_game()

        # ---------- RENDER ----------
        screen.fill(fc.BLACK)
        if game_over:
            screen.fill(fc.TTT_WIN_BG if winner in ("X","O") else fc.TTT_DRAW_BG)

        for r in range(3):
            for c in range(3):
                rect = cell_rect(r,c)
                pygame.draw.rect(screen, fc.TTT_GRID, rect, thickness)
                if board[r][c]:
                    draw_mark(board[r][c], rect)

        if not game_over:
            pygame.draw.rect(screen, fc.WHITE, cell_rect(sel_r, sel_c), thickness)

        if game_over:
            if not fx_started:
                fx_started = True
                if winner in ("X","O"):
                    spawn_confetti()
                    spawn_boom(fc.TTT_LOSE_COLOR[winner])
                else:
                    spawn_boom(fc.WHITE)
            update_particles()
            draw_particles()

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)
