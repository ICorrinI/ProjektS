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

# --- Tetromino Definitions (Rotation = 0 only, Prototype) ---
TETROMINOS = {
    "I": ([[1, 1, 1, 1]], fc.TETRIS_I_LIGHT, fc.TETRIS_I_BASE, fc.TETRIS_I_DARK),
    "T": ([[0,1,0],[1,1,1]], fc.TETRIS_T_LIGHT, fc.TETRIS_T_BASE, fc.TETRIS_T_DARK),
    "L": ([[1,0],[1,0],[1,1]], fc.TETRIS_L_LIGHT, fc.TETRIS_L_BASE, fc.TETRIS_L_DARK),
    "J": ([[0,1],[0,1],[1,1]], fc.TETRIS_J_LIGHT, fc.TETRIS_J_BASE, fc.TETRIS_J_DARK),
    "S": ([[0,1,1],[1,1,0]], fc.TETRIS_S_LIGHT, fc.TETRIS_S_BASE, fc.TETRIS_S_DARK),
    "Z": ([[1,1,0],[0,1,1]], fc.TETRIS_Z_LIGHT, fc.TETRIS_Z_BASE, fc.TETRIS_Z_DARK),
    "O": ([[1,1],[1,1]], fc.TETRIS_O_LIGHT, fc.TETRIS_O_BASE, fc.TETRIS_O_DARK),
}

def tetris_game(screen, matrix, offset_canvas, started_on_pi):
    held_piece = None
    can_hold = True  # verhindert mehrfaches Holden pro Drop

    clock = pygame.time.Clock()

    board = [[None for _ in range(s.TETRIS_COLS)] for _ in range(s.TETRIS_ROWS)]
    score = 0

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
    next_pieces = [new_piece() for _ in range(3)]  # Queue der nächsten 3 Pieces

    def draw_next_pieces():
        for i, p in enumerate(next_pieces):
            shape = p["shape"]
            shape_height = len(shape)
            # vertikales Zentrieren innerhalb des Slots
            top_offset = (s.TETRIS_NEXT_SLOT_HEIGHT - shape_height) // 2

            for y, row in enumerate(shape):
                for x, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            s.TETRIS_NEXT_OFFSET_X + x * s.TETRIS_NEXT_SIZE,
                            int((s.TETRIS_NEXT_OFFSET_Y + i * (s.TETRIS_NEXT_SLOT_HEIGHT * s.TETRIS_NEXT_SIZE + s.TETRIS_NEXT_SPACING) + (y + top_offset) * s.TETRIS_NEXT_SIZE)/20) * 20,
                            s.TETRIS_NEXT_SIZE,
                            s.TETRIS_NEXT_SIZE
                        )
                        pygame.draw.rect(screen, p["colors"][1], rect)

    def draw_hold_piece():
        nonlocal held_piece
        slot_rect = pygame.Rect(
            s.TETRIS_HOLD_OFFSET_X,
            s.TETRIS_HOLD_OFFSET_Y,
            4 * s.TETRIS_NEXT_SIZE,
            4 * s.TETRIS_NEXT_SIZE
        )
        pygame.draw.rect(screen, fc.TETRIS_HOLD, slot_rect, 2)

        if held_piece is None:
            return

        shape = held_piece["shape"]
        shape_height = len(shape)
        shape_width = len(shape[0])

        offset_x = (4 - shape_width) // 2
        offset_y = (4 - shape_height) // 2

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(
                        s.TETRIS_HOLD_OFFSET_X + (x + offset_x) * s.TETRIS_NEXT_SIZE,
                        s.TETRIS_HOLD_OFFSET_Y + (y + offset_y) * s.TETRIS_NEXT_SIZE,
                        s.TETRIS_NEXT_SIZE,
                        s.TETRIS_NEXT_SIZE
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
        nonlocal piece, can_hold
        for y, row in enumerate(piece["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    board[piece["y"] + y][piece["x"] + x] = piece["colors"]
        piece = next_pieces.pop(0)  # Nächstes Piece aus Queue
        can_hold = True
        next_pieces.append(new_piece())  # Neues zufälliges Piece hinten anhängen

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return
                if event.key == pygame.K_UP:
                    piece = tb.try_rotate(piece, board, clockwise=True)
                if event.key == pygame.K_LEFT and can_move(piece["x"] - 1, piece["y"], piece["shape"]):
                    piece["x"] -= 1
                if event.key == pygame.K_RIGHT and can_move(piece["x"] + 1, piece["y"], piece["shape"]):
                    piece["x"] += 1
                if event.key == pygame.K_DOWN:
                    if can_move(piece["x"], piece["y"] + 1, piece["shape"]):
                        piece["y"] += 1
                    else:
                        lock_piece()
                        board[:] = clear_lines()
                if event.key == pygame.K_SPACE:
                    # Move piece all the way down
                    while can_move(piece["x"], piece["y"] + 1, piece["shape"]):
                        piece["y"] += 1
                    lock_piece()
                    board[:] = clear_lines()
                if event.key == pygame.K_c and can_hold:
                    can_hold = False

                    if held_piece is None:
                        held_piece = piece
                        piece = next_pieces.pop(0)
                        next_pieces.append(new_piece())
                    else:
                        held_piece, piece = piece, held_piece

                    # Reset Position des neuen aktiven Pieces
                    piece["x"] = s.TETRIS_COLS // 2 - len(piece["shape"][0]) // 2
                    piece["y"] = 0


        fall_timer += 1
        if fall_timer >= s.TETRIS_FALL_SPEED:
            fall_timer = 0
            if can_move(piece["x"], piece["y"] + 1, piece["shape"]):
                piece["y"] += 1
            else:
                lock_piece()
                board[:] = clear_lines()
                # --- Game Over Check ---
                if not can_move(piece["x"], piece["y"], piece["shape"]):
                    game_over = True
                    while game_over:
                        screen.fill(fc.UI_BG)
                        field_rect = pygame.Rect(
                            s.TETRIS_OFFSET_X,
                            s.TETRIS_OFFSET_Y,
                            s.TETRIS_COLS * s.TETRIS_CELL,
                            s.TETRIS_ROWS * s.TETRIS_CELL
                        )
                        pygame.draw.rect(screen, fc.TETRIS_BG, field_rect)

                        # Draw locked board
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

                        # Draw final score
                        draw_score(screen, score)

                        if started_on_pi:
                            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
                        else:
                            draw_matrix_representation(screen)
                            pygame.display.update()

                        # Warten auf Input zum Neustart
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                piece = new_piece()
                                next_pieces = [new_piece() for _ in range(3)]
                                board[:] = [[None for _ in range(s.TETRIS_COLS)] for _ in range(s.TETRIS_ROWS)]
                                score = 0
                                game_over = False
                            elif event.type == pygame.QUIT:
                                return

                        clock.tick(s.TETRIS_FALL_SPEED)

        # --- Draw Board & Piece ---
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
        draw_next_pieces()  # ← Anzeige der nächsten 3 Pieces

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(s.TETRIS_FALL_SPEED)
