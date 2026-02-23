import random
import pygame

import Settings.settings as s
import Settings.colors as fc
from Settings.output import draw_matrix, draw_matrix_representation
from Settings import inputs


def reaction_runner_game(screen, matrix, offset_canvas, started_on_pi, input_handler):
    clock = pygame.time.Clock()

    PW = s.PIXEL_WIDTH
    GRID = s.RR_GRID

    lane_centers = s.RR_LANE_CENTERS
    lane = s.RR_LANE_START

    # Player sprite/palette aus Settings
    player_sprite = s.RR_PLAYER_SPRITE
    player_palette = fc.RR_PLAYER_PALETTE
    player_w = len(player_sprite[0])
    player_h = len(player_sprite)
    player_y = GRID - player_h - 1

    # Obstacles
    obs_w = s.RR_OBS_W
    obs_h = s.RR_OBS_H

    # Difficulty
    base_speed = s.RR_BASE_SPEED
    speed_gain = s.RR_SPEED_GAIN
    base_spawn = s.RR_BASE_SPAWN
    min_spawn = s.RR_MIN_SPAWN

    # Visuals
    road_color = fc.RR_ROAD_COLOR
    lane_line = fc.RR_LANE_LINE
    obstacle_color = fc.RR_OBSTACLE

    # Score font aus Settings
    FONT_3x5 = s.RR_FONT_3X5

    def clamp(v, lo, hi):
        return max(lo, min(hi, v))

    def rect_from_grid(mx, my, mw, mh):
        return pygame.Rect(mx * PW, my * PW, mw * PW, mh * PW)

    def draw_sprite(sprite, mx, my, palette):
        for sy, row in enumerate(sprite):
            for sx, val in enumerate(row):
                if val == 0:
                    continue
                pygame.draw.rect(screen, palette[val], rect_from_grid(mx + sx, my + sy, 1, 1))

    def draw_char(ch: str, mx: int, my: int, color):
        glyph = FONT_3x5.get(ch, FONT_3x5[" "])
        for gy in range(5):
            for gx in range(3):
                if glyph[gy][gx]:
                    pygame.draw.rect(screen, color, rect_from_grid(mx + gx, my + gy, 1, 1))

    def draw_text(text: str, mx: int, my: int, color):
        x = mx
        for ch in text:
            draw_char(ch, x, my, color)
            x += 4  # 3 breit + 1 spacing (in grid coords)

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
        input_handler.process_events(pygame.event.get())

        if input_handler.is_pressed(inputs.BACK):
            return

        now = pygame.time.get_ticks()
        dt = clock.get_time() / 1000.0

        survived_s = (now - state["start_ms"]) / 1000.0
        level = int(survived_s // s.RR_LEVEL_SECONDS)

        speed = base_speed + level * speed_gain
        spawn_every = clamp(base_spawn - level * s.RR_SPAWN_DECAY_PER_LEVEL, min_spawn, 5.0)

        # INPUT
        if state["alive"]:
            if input_handler.is_pressed(inputs.LEFT):
                lane = max(0, lane - 1)
            if input_handler.is_pressed(inputs.RIGHT):
                lane = min(2, lane + 1)
        else:
            if input_handler.is_pressed(inputs.CONFIRM):
                lane = s.RR_LANE_START
                state = new_run()

        # UPDATE
        if state["alive"]:
            if (now - state["last_spawn_ms"]) / 1000.0 >= spawn_every:
                state["last_spawn_ms"] = now
                chosen = random.randint(0, 2)
                if random.random() < s.RR_PLAYER_LANE_SPAWN_CHANCE:
                    chosen = lane
                state["obstacles"].append({"lane": chosen, "y": -float(obs_h)})

            for o in state["obstacles"]:
                o["y"] += speed * dt

            kept = []
            for o in state["obstacles"]:
                if o["y"] > GRID:
                    state["score"] += 1
                else:
                    kept.append(o)
            state["obstacles"] = kept

            # HITBOX (kleiner als Sprite)
            px = lane_centers[lane] - (player_w // 2)
            hit_x = px + s.RR_HITBOX_INSET_X
            hit_y = player_y + s.RR_HITBOX_INSET_Y
            hit_w = max(1, player_w - s.RR_HITBOX_SHRINK_W)
            hit_h = max(1, player_h - s.RR_HITBOX_SHRINK_H)
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

        # Road (optional): wenn du komplett schwarz willst -> RR_ROAD_COLOR = BLACK setzen
        pygame.draw.rect(screen, road_color, (0, 0, s.SCREEN_WIDTH, s.SCREEN_HEIGHT))

        # Lane lines
        pygame.draw.rect(screen, lane_line, rect_from_grid(s.RR_LANE_SEP_1, 0, 1, GRID))
        pygame.draw.rect(screen, lane_line, rect_from_grid(s.RR_LANE_SEP_2, 0, 1, GRID))

        # Obstacles
        for o in state["obstacles"]:
            ox = lane_centers[o["lane"]] - (obs_w // 2)
            oy = int(round(o["y"]))
            if -10 <= oy <= GRID + 5:
                pygame.draw.rect(screen, obstacle_color, rect_from_grid(ox, oy, obs_w, obs_h))

        # Player
        px = lane_centers[lane] - (player_w // 2)
        draw_sprite(player_sprite, px, player_y, player_palette)

        # SCORE: NUR OBEN LINKS
        score_val = min(state["score"], 99)
        tens = score_val // 10
        ones = score_val % 10
        draw_text(str(tens), s.RR_SCORE_X, s.RR_SCORE_Y, fc.RR_SCORE_COLOR)
        draw_text(str(ones), s.RR_SCORE_X + 4, s.RR_SCORE_Y, fc.RR_SCORE_COLOR)

        # GAME OVER: Hintergrund schwarz + Score in der Mitte (optional)
        if not state["alive"]:
            screen.fill(fc.BLACK)

            if s.RR_SHOW_SCORE_ON_GAME_OVER:
                draw_text(str(tens), s.RR_GAMEOVER_SCORE_X, s.RR_GAMEOVER_SCORE_Y, fc.WHITE)
                draw_text(str(ones), s.RR_GAMEOVER_SCORE_X + 4, s.RR_GAMEOVER_SCORE_Y, fc.WHITE)

            # kleiner Boden-Strich wie bei euren anderen Games
            pygame.draw.rect(screen, fc.WHITE, (0, s.SCREEN_HEIGHT - PW, s.SCREEN_WIDTH, PW))

        # OUTPUT
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(30)
