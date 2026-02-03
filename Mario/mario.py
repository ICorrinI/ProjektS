import pygame
import json
from Settings.output import draw_matrix_representation, draw_matrix, draw_shaded_block
from Settings.colors import *
from Settings.settings import (
    SCREEN_WIDTH,
    PIXEL_WIDTH,
    MARIO_WORLD,
    SCROLL_BORDER,
    ACCEL_TIME,
    MAX_SPEED_MULTIPLIER,
    BASE_SPEED,
    SPAWN_TILE_X,
    SPAWN_TILE_Y,
    GRAVITY,
    JUMP_VELOCITY,
    INPUT_DELAY,
)
from Settings import inputs


def mario_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    part_name = "part1"
    clock = pygame.time.Clock()

    # -----------------------------
    # WORLD
    # -----------------------------
    with open(MARIO_WORLD, "r") as f:
        world_data = json.load(f)

    part = world_data["parts"][part_name]
    world_map = part["map"]
    palette = {int(k): tuple(v) for k, v in part["palette"].items()}

    MAP_HEIGHT = len(world_map)
    MAP_WIDTH = len(world_map[0])
    WORLD_PIXEL_WIDTH = MAP_WIDTH * PIXEL_WIDTH
    WORLD_PIXEL_HEIGHT = MAP_HEIGHT * PIXEL_WIDTH

    camera_x = 0
    DEATH_Y = 32 * PIXEL_WIDTH  # Grenze nach unten

    # -----------------------------
    # PLAYER
    # -----------------------------
    class Player:
        def __init__(self):
            self.reset()

        def reset(self):
            self.tile_x = SPAWN_TILE_X
            self.tile_y = SPAWN_TILE_Y if SPAWN_TILE_Y is not None else MAP_HEIGHT - 1
            self.x = self.tile_x * PIXEL_WIDTH
            self.y = self.tile_y * PIXEL_WIDTH

            self.direction = 0
            self.hold_time = 0.0

            self.vy = 0  # vertikale Geschwindigkeit
            self.on_ground = False

            self.rect = pygame.Rect(self.x, self.y, PIXEL_WIDTH, PIXEL_WIDTH)

        @property
        def world_x(self):
            return self.x

        @property
        def world_y(self):
            return self.y

        def update(self, dt, world_map):
            # -----------------
            # Horizontale Bewegung: Snap-to-Grid
            # -----------------
            if self.direction != 0:
                next_tile_x = self.tile_x + self.direction
                if 0 <= next_tile_x < len(world_map[0]):
                    if world_map[self.tile_y][next_tile_x] == 0:
                        self.tile_x = next_tile_x
                        self.x = self.tile_x * PIXEL_WIDTH

            # -----------------
            # Vertikale Bewegung (Gravitation)
            # -----------------
            self.vy += GRAVITY * dt
            new_y = self.y + self.vy * dt

            # -----------------
            # Death-Border unten
            # -----------------
            if new_y >= DEATH_Y:
                self.reset()  # sofort zurücksetzen
                return  # wichtig, damit keine Kollisionen mehr geprüft werden

            future_rect = pygame.Rect(self.x, new_y, PIXEL_WIDTH, PIXEL_WIDTH)
            left_tile = int(future_rect.left // PIXEL_WIDTH)
            right_tile = int((future_rect.right - 1) // PIXEL_WIDTH)
            top_tile = int(future_rect.top // PIXEL_WIDTH)
            bottom_tile = int((future_rect.bottom - 1) // PIXEL_WIDTH)

            self.on_ground = False

            # Prüfe Kollision unten
            for tx in range(left_tile, right_tile + 1):
                if bottom_tile < len(world_map) and world_map[bottom_tile][tx] != 0:
                    new_y = bottom_tile * PIXEL_WIDTH - PIXEL_WIDTH
                    self.vy = 0
                    self.on_ground = True
                    break

            # Prüfe Kollision oben
            for tx in range(left_tile, right_tile + 1):
                if top_tile >= 0 and world_map[top_tile][tx] != 0:
                    new_y = (top_tile + 1) * PIXEL_WIDTH
                    self.vy = 0
                    break

            self.y = new_y
            self.tile_y = int(self.y // PIXEL_WIDTH)
            self.rect.topleft = (self.x, self.y)

        def jump(self):
            if self.on_ground:
                self.vy = -JUMP_VELOCITY
                self.on_ground = False

    player = Player()

    # -----------------------------
    # GAME LOOP
    # -----------------------------
    run = True
    while run:
        dt = clock.tick(60) / 1000.0

        # -----------------------------
        # UPDATE PLAYER ZUERST
        # -----------------------------
        player.update(dt, world_map)

        # -----------------------------
        # INPUT
        # -----------------------------
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed_custom(inputs.BACK, INPUT_DELAY):
            return

        # Horizontal bewegen mit Delay
        player.direction = 0
        if input_handler.is_pressed_custom(inputs.LEFT, INPUT_DELAY):
            player.direction = -1
        elif input_handler.is_pressed_custom(inputs.RIGHT, INPUT_DELAY):
            player.direction = 1

        # Jump sofort, nur wenn player.on_ground ist
        if inputs.CONFIRM in input_handler.pressed or inputs.UP in input_handler.pressed:
            player.jump()

        # -----------------------------
        # CAMERA MIT LINKS + RECHTS SCROLL
        # -----------------------------
        player_screen_x = player.world_x - camera_x

        left_scroll_border = SCREEN_WIDTH * 0.4  # 40% vom linken Rand
        right_scroll_border = SCREEN_WIDTH * 0.6 # 60% vom rechten Rand

        # Scroll nach rechts
        if player_screen_x > right_scroll_border:
            camera_x += player_screen_x - right_scroll_border
        # Scroll nach links
        elif player_screen_x < left_scroll_border:
            camera_x -= left_scroll_border - player_screen_x

        # Clamp Camera
        camera_x = max(0, min(camera_x, WORLD_PIXEL_WIDTH - SCREEN_WIDTH))

        # -----------------------------
        # RENDER
        # -----------------------------
        screen.fill((0, 0, 0))

        for y, row in enumerate(world_map):
            for x, tile_id in enumerate(row):
                if tile_id == 0:
                    continue
                color = palette[tile_id]
                world_x = x * PIXEL_WIDTH
                screen_x = world_x - camera_x
                if -PIXEL_WIDTH <= screen_x <= SCREEN_WIDTH:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(screen_x, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH),
                    )

        # Player zeichnen
        draw_shaded_block(
            screen,
            pygame.Rect(int(player.world_x - camera_x), int(player.world_y), PIXEL_WIDTH, PIXEL_WIDTH),
            (255, 120, 120),
            (200, 0, 0),
            (120, 0, 0),
        )

        # Matrix Output
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()
