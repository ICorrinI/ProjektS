import random
import pygame

import Settings.settings as s
import Settings.colors as fc
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def stack_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    """
    STACK / TIMING TOWER (Singleplayer)

    - Block fährt links <-> rechts
    - CONFIRM setzt Block ab
    - Überlappung bleibt stehen, Rest wird abgeschnitten
    - Wenn keine Überlappung: Game Over
    - Speed steigt mit Höhe
    - Score = Höhe (0..99)
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

    # Farbwahl: pro Layer zyklisch
    def layer_color(layer_index: int):
        colors = fc.STACK_BLOCK_COLORS
        return colors[layer_index % len(colors)]

    # --- game state ---
    def new_run():
        start_w = s.STACK_START_WIDTH
        start_y = GRID - 1
        return {
            "alive": True,
            "score": 0,
            # tower items: (x, y, w, color)
            "tower": [],
            "cur_y": start_y,
            "cur_w": start_w,
            "cur_x": 0.0,
            "dir": 1,  # 1 right, -1 left
            "speed": float(s.STACK_BASE_SPEED),  # cells per second
        }

    state = new_run()

    # Init: erste Basis in der Mitte “fest”
    base_x = (GRID - state["cur_w"]) // 2
    state["tower"].append((base_x, state["cur_y"], state["cur_w"], layer_color(0)))
    state["cur_y"] -= 1
    state["cur_x"] = 0.0
    state["dir"] = 1

    while True:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        dt = clock.get_time() / 1000.0

        # restart on game over
        if not state["alive"]:
            if input_handler.is_pressed(inputs.CONFIRM):
                state = new_run()
                base_x = (GRID - state["cur_w"]) // 2
                state["tower"].append((base_x, state["cur_y"], state["cur_w"], layer_color(0)))
                state["cur_y"] -= 1
                state["cur_x"] = 0.0
                state["dir"] = 1
            else:
                # render game over screen
                screen.fill(fc.STACK_BG)
                draw_2digit(state["score"], s.STACK_SCORE_X, s.STACK_SCORE_Y, fc.STACK_SCORE_COLOR)
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

        # move current block (left/right)
        max_x = GRID - state["cur_w"]
        state["cur_x"] += state["dir"] * state["speed"] * dt
        if state["cur_x"] <= 0:
            state["cur_x"] = 0.0
            state["dir"] = 1
        elif state["cur_x"] >= max_x:
            state["cur_x"] = float(max_x)
            state["dir"] = -1

        # drop block
        if input_handler.is_pressed(inputs.CONFIRM):
            cur_x_int = int(round(state["cur_x"]))
            cur_w = state["cur_w"]
            cur_y = state["cur_y"]

            last_x, last_y, last_w, _last_col = state["tower"][-1]

            left = max(cur_x_int, last_x)
            right = min(cur_x_int + cur_w, last_x + last_w)
            overlap = right - left

            if overlap <= 0:
                state["alive"] = False
            else:
                placed_x = left
                placed_w = overlap

                # color for this placed layer = based on score+1 (weil score zählt placed layers nach base)
                next_layer_index = len(state["tower"])  # base was layer 0, next is 1,2,3...
                placed_color = layer_color(next_layer_index)

                state["tower"].append((placed_x, cur_y, placed_w, placed_color))
                state["score"] = clamp(state["score"] + 1, 0, 99)

                # next row
                state["cur_y"] -= 1
                state["cur_w"] = placed_w

                # speed up slightly
                state["speed"] = min(
                    float(s.STACK_MAX_SPEED),
                    float(s.STACK_BASE_SPEED) + state["score"] * float(s.STACK_SPEED_GAIN)
                )

                # if reached top: wrap endless (shift tower down)
                if state["cur_y"] < 0:
                    state["tower"] = [(x, y + 1, w, col) for (x, y, w, col) in state["tower"] if y + 1 < GRID]
                    state["cur_y"] = 0

                # new moving block start position
                if random.random() < 0.5:
                    state["cur_x"] = 0.0
                    state["dir"] = 1
                else:
                    state["cur_x"] = float(GRID - state["cur_w"])
                    state["dir"] = -1

        # --- render ---
        screen.fill(fc.STACK_BG)

        # guide lines
        for gx in s.STACK_GUIDE_XS:
            pygame.draw.rect(screen, fc.STACK_GUIDE_COLOR, rect_from_grid(gx, 0, 1, GRID))

        # draw placed tower blocks (with their colors)
        for (x, y, w, col) in state["tower"]:
            pygame.draw.rect(screen, col, rect_from_grid(x, y, w, 1))

        # draw moving block (use next layer color too)
        cur_x_int = int(round(state["cur_x"]))
        active_layer_index = len(state["tower"])  # next placed layer
        active_color = layer_color(active_layer_index)
        pygame.draw.rect(screen, active_color, rect_from_grid(cur_x_int, state["cur_y"], state["cur_w"], 1))

        # score top-left
        draw_2digit(state["score"], s.STACK_SCORE_X, s.STACK_SCORE_Y, fc.STACK_SCORE_COLOR)

        # output
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(s.STACK_FPS)