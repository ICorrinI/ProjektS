import pygame
import random

import Settings.settings as s
import Settings.colors as fc
from Settings.output import (
    draw_matrix,
    draw_matrix_representation,
    draw_score_tetris,
    draw_shaded_block,
    draw_score
)
from . import turnblock as tb
from Settings import inputs

# --- Tetromino Definitions ---
TETROMINOS = {
    "I": ([[1, 1, 1, 1]], fc.TETRIS_I_LIGHT, fc.TETRIS_I_BASE, fc.TETRIS_I_DARK),
    "T": ([[0, 1, 0], [1, 1, 1]], fc.TETRIS_T_LIGHT, fc.TETRIS_T_BASE, fc.TETRIS_T_DARK),
    "L": ([[1, 0], [1, 0], [1, 1]], fc.TETRIS_L_LIGHT, fc.TETRIS_L_BASE, fc.TETRIS_L_DARK),
    "J": ([[0, 1], [0, 1], [1, 1]], fc.TETRIS_J_LIGHT, fc.TETRIS_J_BASE, fc.TETRIS_J_DARK),
    "S": ([[0, 1, 1], [1, 1, 0]], fc.TETRIS_S_LIGHT, fc.TETRIS_S_BASE, fc.TETRIS_S_DARK),
    "Z": ([[1, 1, 0], [0, 1, 1]], fc.TETRIS_Z_LIGHT, fc.TETRIS_Z_BASE, fc.TETRIS_Z_DARK),
    "O": ([[1, 1], [1, 1]], fc.TETRIS_O_LIGHT, fc.TETRIS_O_BASE, fc.TETRIS_O_DARK),
}


def tetris_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()

    board = [[None for _ in range(s.TETRIS_COLS)] for _ in range(s.TETRIS_ROWS)]
    score = 0

    held_piece = None
    can_hold = True

    def new_piece():
        key = random.choice(list(TETROMINOS.keys()))
        shape, light, base, dark = TETROMINOS[key]
        return {
            "shape": shape,
            "x": s.TETRIS_COLS // 2 - len(shape[0]) // 2,
            "y": 0,
            "colors": (light, base, dark),
            "type": key,
            "rotation": 0
        }

    piece = new_piece()
    next_pieces = [new_piece() for _ in range(3)]

    def is_game_over(p):
        return not can_move(p["x"], p["y"], p["shape"])

    def draw_next_pieces():
        for i, p in enumerate(next_pieces):
            shape = p["shape"]
            h = len(shape)
            offset_y = (s.TETRIS_NEXT_SLOT_HEIGHT - h) // 2
            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            s.TETRIS_NEXT_OFFSET_X + x * s.TETRIS_NEXT_SIZE,
                            s.TETRIS_NEXT_OFFSET_Y
                            + i * (s.TETRIS_NEXT_SLOT_HEIGHT * s.TETRIS_NEXT_SIZE + s.TETRIS_NEXT_SPACING)
                            + (y + offset_y) * s.TETRIS_NEXT_SIZE,
                            s.TETRIS_NEXT_SIZE,
                            s.TETRIS_NEXT_SIZE
                        )
                        pygame.draw.rect(screen, p["colors"][1], rect)

    def draw_hold_piece():
        nonlocal held_piece
        PREVIEW_SIZE = s.TETRIS_NEXT_SIZE
        SLOT_SIZE = 4 * PREVIEW_SIZE

        slot_rect = pygame.Rect(
            s.TETRIS_HOLD_OFFSET_X,
            s.TETRIS_HOLD_OFFSET_Y,
            SLOT_SIZE,
            SLOT_SIZE
        )

        pygame.draw.rect(screen, fc.UI_BG, slot_rect)
        pygame.draw.rect(screen, fc.TETRIS_HOLD, slot_rect, 0)

        if held_piece is None:
            return

        shape = held_piece["shape"]
        h = len(shape)
        w = len(shape[0])
        offset_x = (4 - w) // 2
        offset_y = (4 - h) // 2

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        s.TETRIS_HOLD_OFFSET_X + (x + offset_x) * PREVIEW_SIZE,
                        s.TETRIS_HOLD_OFFSET_Y + (y + offset_y) * PREVIEW_SIZE,
                        PREVIEW_SIZE,
                        PREVIEW_SIZE
                    )
                    pygame.draw.rect(screen, held_piece["colors"][1], rect)

    def can_move(px, py, shape):
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                bx = px + x
                by = py + y
                if bx < 0 or bx >= s.TETRIS_COLS or by >= s.TETRIS_ROWS:
                    return False
                if by >= 0 and board[by][bx] is not None:
                    return False
        return True

    def lock_piece():
        nonlocal piece, can_hold, run
        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    board[piece["y"] + y][piece["x"] + x] = piece["colors"]
        piece = next_pieces.pop(0)
        next_pieces.append(new_piece())
        can_hold = True
        if is_game_over(piece):
            run = False  # Game Over

    def clear_lines():
        nonlocal score
        new_board = [row for row in board if any(cell is None for cell in row)]
        cleared = s.TETRIS_ROWS - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [None] * s.TETRIS_COLS)
        score += cleared
        return new_board

    fall_timer = 0
    run = True

    while run:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        if input_handler.is_pressed(inputs.UP):
            piece = tb.try_rotate(piece, board, clockwise=True)

        if input_handler.is_pressed(inputs.LEFT) and can_move(piece["x"] - 1, piece["y"], piece["shape"]):
            piece["x"] -= 1

        if input_handler.is_pressed(inputs.RIGHT) and can_move(piece["x"] + 1, piece["y"], piece["shape"]):
            piece["x"] += 1

        if input_handler.is_pressed(inputs.DOWN):
            if can_move(piece["x"], piece["y"] + 1, piece["shape"]):
                piece["y"] += 1
            else:
                lock_piece()
                board[:] = clear_lines()

        if input_handler.is_pressed(inputs.DROP):
            while can_move(piece["x"], piece["y"] + 1, piece["shape"]):
                piece["y"] += 1
            lock_piece()
            board[:] = clear_lines()

        if input_handler.is_pressed(inputs.HOLD) and can_hold:
            can_hold = False
            if held_piece is None:
                held_piece = piece
                piece = next_pieces.pop(0)
                next_pieces.append(new_piece())
            else:
                held_piece, piece = piece, held_piece
            piece["x"] = s.TETRIS_COLS // 2 - len(piece["shape"][0]) // 2
            piece["y"] = 0
            if is_game_over(piece):
                run = False  # Game Over

        # Fall-Timer
        fall_timer += 1
        if fall_timer >= s.TETRIS_FALL_SPEED:
            fall_timer = 0
            if can_move(piece["x"], piece["y"] + 1, piece["shape"]):
                piece["y"] += 1
            else:
                lock_piece()
                board[:] = clear_lines()

        # Render
        screen.fill(fc.UI_BG)
        field_rect = pygame.Rect(
            s.TETRIS_OFFSET_X,
            s.TETRIS_OFFSET_Y,
            s.TETRIS_COLS * s.TETRIS_CELL,
            s.TETRIS_ROWS * s.TETRIS_CELL
        )
        pygame.draw.rect(screen, fc.TETRIS_BG, field_rect)

        for y in range(s.TETRIS_ROWS):
            for x in range(s.TETRIS_COLS):
                if board[y][x]:
                    rect = pygame.Rect(
                        s.TETRIS_OFFSET_X + x * s.TETRIS_CELL,
                        s.TETRIS_OFFSET_Y + y * s.TETRIS_CELL,
                        s.TETRIS_CELL,
                        s.TETRIS_CELL
                    )
                    draw_shaded_block(screen, rect, *board[y][x])

        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        s.TETRIS_OFFSET_X + (piece["x"] + x) * s.TETRIS_CELL,
                        s.TETRIS_OFFSET_Y + (piece["y"] + y) * s.TETRIS_CELL,
                        s.TETRIS_CELL,
                        s.TETRIS_CELL
                    )
                    draw_shaded_block(screen, rect, *piece["colors"])

        draw_score_tetris(screen, score)
        draw_hold_piece()
        draw_next_pieces()

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(s.TETRIS_FALL_SPEED)

    # Game Over Screen
    pygame.display.update()
    pygame.time.wait(2000)  # 2 Sekunden Pause
