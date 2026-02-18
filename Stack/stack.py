import random
import pygame

import Settings.settings as s
import Settings.colors as fc
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def stack_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    """
    STACK / TIMING TOWER (Singleplayer)

    Idee:
      - Ein Block fährt links <-> rechts
      - CONFIRM droppt den Block
      - Überlappung bleibt stehen, Rest wird abgeschnitten
      - Wenn keine Überlappung: Game Over
      - Speed steigt mit Höhe
      - Score = Höhe (0..99)

    Controls:
      - LEFT/RIGHT optional: Richtung flip (nice feeling)
      - CONFIRM: drop
      - BACK: zurück ins Menü
    """

    clock = pygame.time.Clock()

    PW = s.PIXEL_WIDTH
    GRID = s.STACK_GRID  # 32

    # --- helpers ---
    def rect_from_grid(mx, my, mw, mh):
        return pygame.Rect(mx * PW, my * PW, mw * PW, mh * PW)

    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    # 3x5 digits (nur 0-9 + space)
    FONT_3x5 = {
        "0": [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
        "1": [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
        "2": [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
        "3": [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],
        "4": [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
        "5": [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
        "6": [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
        "7": [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0]],
        "8": [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
        "9": [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]],
        " ": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
    }

    def draw_char(ch: str, mx: int, my: int, color):
        glyph = FONT_3x5.get(ch, FONT_3x5[" "])
        for gy in range(5):
            for gx in range(3):
                if glyph[gy][gx]:
                    pygame.draw.rect(screen, color, rect_from_grid(mx + gx, my + gy, 1, 1))

    def draw_2digit(number: int, mx: int, my: int, color):
        number = clamp(number, 0, 99)
        tens = number // 10
        ones = number % 10
        draw_char(str(tens), mx, my, color)
        draw_char(str(ones), mx + 4, my, color)  # 3 + 1 spacing

    # --- game state ---
    def new_run():
        start_w = s.STACK_START_WIDTH
        start_y = GRID - 1
        return {
            "alive": True,
            "score": 0,
            "tower": [],  # list of (x, y, w)
            "cur_y": start_y,
            "cur_w": start_w,
            "cur_x": 0,
            "dir": 1,  # 1 right, -1 left
            "speed": s.STACK_BASE_SPEED,  # cells per second
            "last_ms": pygame.time.get_ticks(),
            "shake_ms": 0,
        }

    state = new_run()

    # Init: erste Basis in der Mitte “fest”
    base_x = (GRID - state["cur_w"]) // 2
    state["tower"].append((base_x, state["cur_y"], state["cur_w"]))
    state["cur_y"] -= 1
    state["cur_x"] = 0
    state["dir"] = 1

    while True:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        now = pygame.time.get_ticks()
        dt = clock.get_time() / 1000.0

        # restart on game over
        if not state["alive"]:
            if input_handler.is_pressed(inputs.CONFIRM):
                state = new_run()
                base_x = (GRID - state["cur_w"]) // 2
                state["tower"].append((base_x, state["cur_y"], state["cur_w"]))
                state["cur_y"] -= 1
                state["cur_x"] = 0
                state["dir"] = 1
            else:
                # render game over screen
                screen.fill(fc.STACK_BG)
                # show final score top-left
                draw_2digit(state["score"], s.STACK_SCORE_X, s.STACK_SCORE_Y, fc.STACK_SCORE_COLOR)
                # small border line bottom (like your style)
                pygame.draw.rect(screen, fc.WHITE, (0, s.SCREEN_HEIGHT - PW, s.SCREEN_WIDTH, PW))

                if started_on_pi:
                    offset_canvas = draw_matrix(screen, matrix, offset_canvas)
                else:
                    draw_matrix_representation(screen)
                    pygame.display.update()

                clock.tick(s.STACK_FPS)
                continue

        # optional: flip direction for nicer control feel
        if input_handler.is_pressed(inputs.LEFT) or input_handler.is_pressed(inputs.RIGHT):
            state["dir"] *= -1

        # move current block
        max_x = GRID - state["cur_w"]
        state["cur_x"] += state["dir"] * state["speed"] * dt
        if state["cur_x"] <= 0:
            state["cur_x"] = 0
            state["dir"] = 1
        elif state["cur_x"] >= max_x:
            state["cur_x"] = max_x
            state["dir"] = -1

        # drop block
        if input_handler.is_pressed(inputs.CONFIRM):
            cur_x_int = int(round(state["cur_x"]))
            cur_w = state["cur_w"]
            cur_y = state["cur_y"]

            # compare with last placed
            last_x, last_y, last_w = state["tower"][-1]

            # overlap interval
            left = max(cur_x_int, last_x)
            right = min(cur_x_int + cur_w, last_x + last_w)
            overlap = right - left

            if overlap <= 0:
                state["alive"] = False
            else:
                # place trimmed block
                placed_x = left
                placed_w = overlap
                state["tower"].append((placed_x, cur_y, placed_w))

                state["score"] = clamp(state["score"] + 1, 0, 99)

                # next row
                state["cur_y"] -= 1
                state["cur_w"] = placed_w

                # speed up slightly
                state["speed"] = min(
                    s.STACK_MAX_SPEED,
                    s.STACK_BASE_SPEED + state["score"] * s.STACK_SPEED_GAIN
                )

                # if reached top: wrap (continue endless, but keep last rows)
                if state["cur_y"] < 0:
                    # shift tower down by 1 (drop oldest)
                    # keep it visually stable & endless
                    state["tower"] = [(x, y + 1, w) for (x, y, w) in state["tower"] if y + 1 < GRID]
                    state["cur_y"] = 0

                # new moving block start position
                # alternate start side for variety
                if random.random() < 0.5:
                    state["cur_x"] = 0
                    state["dir"] = 1
                else:
                    state["cur_x"] = GRID - state["cur_w"]
                    state["dir"] = -1

        # --- render ---
        screen.fill(fc.STACK_BG)

        # optional lane/guide lines (subtle vertical guides)
        for gx in s.STACK_GUIDE_XS:
            pygame.draw.rect(screen, fc.STACK_GUIDE_COLOR, rect_from_grid(gx, 0, 1, GRID))

        # draw placed tower blocks
        for (x, y, w) in state["tower"]:
            pygame.draw.rect(screen, fc.STACK_BLOCK, rect_from_grid(x, y, w, 1))

        # draw moving block
        cur_x_int = int(round(state["cur_x"]))
        pygame.draw.rect(screen, fc.STACK_BLOCK_ACTIVE, rect_from_grid(cur_x_int, state["cur_y"], state["cur_w"], 1))

        # score top-left (00..99)
        draw_2digit(state["score"], s.STACK_SCORE_X, s.STACK_SCORE_Y, fc.STACK_SCORE_COLOR)

        # output
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(s.STACK_FPS)
