import random
import pygame

import Settings.settings as s
import Settings.colors as fc
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def reaction_runner_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()

    PW = s.PIXEL_WIDTH
    GRID = 32

    lane_centers = [8, 16, 24]
    lane = 1

    # --- Player Sprite (Mini-Auto) ---
    # 0=transparent, 1=gelb, 2=fensterblau, 3=reifen
    player_sprite = [
        [0, 1, 1, 1, 0],
        [1, 2, 2, 2, 1],
        [1, 1, 1, 1, 1],
        [3, 0, 0, 0, 3],
    ]
    player_w = len(player_sprite[0])
    player_h = len(player_sprite)
    player_y = GRID - player_h - 1

    # Obstacles
    obs_w = 2
    obs_h = 2

    # Spawn/Speed
    base_speed = 7.0
    speed_gain = 0.55
    base_spawn = 0.85
    min_spawn = 0.28

    # Visuals
    road_color = fc.DARK_GRAY
    lane_line = fc.GRAY
    obstacle_color = fc.RED

    # Car colors
    CAR_YELLOW = (255, 235, 0)
    WINDOW_BLUE = (80, 200, 255)
    TIRE_GRAY = (200, 200, 200)
    player_palette = {
        1: CAR_YELLOW,
        2: WINDOW_BLUE,
        3: TIRE_GRAY,
    }

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

    def draw_char(ch: str, mx: int, my: int, color):
        glyph = FONT_3x5.get(ch, FONT_3x5[" "])
        for gy in range(5):
            for gx in range(3):
                if glyph[gy][gx]:
                    x = (mx + gx) * PW
                    y = (my + gy) * PW
                    pygame.draw.rect(screen, color, (x, y, PW, PW))

    def draw_text(text: str, mx: int, my: int, color):
        x = mx
        for ch in text:
            draw_char(ch, x, my, color)
            x += 4

    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def rect_from_grid(mx, my, mw, mh):
        return pygame.Rect(mx * PW, my * PW, mw * PW, mh * PW)

    def draw_sprite(sprite, mx, my, palette):
        for sy, row in enumerate(sprite):
            for sx, val in enumerate(row):
                if val == 0:
                    continue
                pygame.draw.rect(
                    screen,
                    palette[val],
                    rect_from_grid(mx + sx, my + sy, 1, 1)
                )

    # --- Game state ---
    def new_run():
        return {
            "obstacles": [],
            "alive": True,
            "score": 0,
            "start_ms": pygame.time.get_ticks(),
            "last_spawn_ms": pygame.time.get_ticks(),
        }

    state = new_run()

    while True:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        now = pygame.time.get_ticks()
        dt = clock.get_time() / 1000.0

        survived_s = (now - state["start_ms"]) / 1000.0
        level = int(survived_s // 6)
        speed = base_speed + level * speed_gain
        spawn_every = clamp(base_spawn - level * 0.06, min_spawn, 5.0)

        # INPUT
        if state["alive"]:
            if input_handler.is_pressed(inputs.LEFT):
                lane = max(0, lane - 1)
            if input_handler.is_pressed(inputs.RIGHT):
                lane = min(2, lane + 1)
        else:
            if input_handler.is_pressed(inputs.CONFIRM):
                lane = 1
                state = new_run()

        # UPDATE
        if state["alive"]:
            if (now - state["last_spawn_ms"]) / 1000.0 >= spawn_every:
                state["last_spawn_ms"] = now
                chosen = random.randint(0, 2)
                if random.random() < 0.2:
                    chosen = lane
                state["obstacles"].append({"lane": chosen, "y": -2.0})

            for o in state["obstacles"]:
                o["y"] += speed * dt

            kept = []
            for o in state["obstacles"]:
                if o["y"] > GRID:
                    state["score"] += 1
                else:
                    kept.append(o)
            state["obstacles"] = kept

            # --- FAIR HITBOX (kleiner als Sprite) ---
            px = lane_centers[lane] - (player_w // 2)

            # hitbox: 1 pixel Rand weg + Reifen unten nicht zählen lassen
            hit_x = px + 1
            hit_y = player_y + 1
            hit_w = max(1, player_w - 2)
            hit_h = max(1, player_h - 2)

            player_rect = pygame.Rect(hit_x, hit_y, hit_w, hit_h)

            for o in state["obstacles"]:
                ox = lane_centers[o["lane"]] - (obs_w // 2)
                oy = int(round(o["y"]))
                obs_rect = pygame.Rect(ox, oy, obs_w, obs_h)
                if player_rect.colliderect(obs_rect):
                    state["alive"] = False
                    break

        # RENDER
        screen.fill(fc.BLACK)
        pygame.draw.rect(screen, road_color, (0, 0, s.SCREEN_WIDTH, s.SCREEN_HEIGHT))

        sep1, sep2 = 12, 20
        pygame.draw.rect(screen, lane_line, rect_from_grid(sep1, 0, 1, GRID))
        pygame.draw.rect(screen, lane_line, rect_from_grid(sep2, 0, 1, GRID))

        for o in state["obstacles"]:
            ox = lane_centers[o["lane"]] - (obs_w // 2)
            oy = int(round(o["y"]))
            if -5 <= oy <= 35:
                pygame.draw.rect(screen, obstacle_color, rect_from_grid(ox, oy, obs_w, obs_h))

        px = lane_centers[lane] - (player_w // 2)
        draw_sprite(player_sprite, px, player_y, player_palette)

        # Score nur 2 digits
        score_val = min(state["score"], 99)
        tens = score_val // 10
        ones = score_val % 10
        draw_text(str(tens), 1, 1, fc.BLACK)
        draw_text(str(ones), 5, 1, fc.BLACK)

        if not state["alive"]:
            blink = ((now // 180) % 2) == 0
            if blink:
                screen.fill(fc.RED)
            draw_text(str(tens), 12, 17, fc.WHITE)
            draw_text(str(ones), 16, 17, fc.WHITE)
            pygame.draw.rect(screen, fc.WHITE, (0, s.SCREEN_HEIGHT - PW, s.SCREEN_WIDTH, PW))

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)

