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
)
from Settings import inputs


def mario_game(
    screen,
    matrix,
    offset_canvas,
    started_on_pi,
    input_handler: inputs.InputHandler,
):
    part_name = "part1"
    clock = pygame.time.Clock()

    # -----------------------------
    # LOAD WORLD
    # -----------------------------
    with open(MARIO_WORLD, "r") as f:
        world_data = json.load(f)

    part = world_data["parts"][part_name]
    world_map = part["map"]
    palette = {int(k): tuple(v) for k, v in part["palette"].items()}

    MAP_HEIGHT = len(world_map)
    MAP_WIDTH = len(world_map[0])
    WORLD_PIXEL_WIDTH = MAP_WIDTH * PIXEL_WIDTH

    camera_x = 0

    # -----------------------------
    # PLAYER
    # -----------------------------
    class Player:
        def __init__(self):
            self.reset()

        def reset(self):
            self.tile_x = 0
            self.y = (MAP_HEIGHT - 1) * PIXEL_WIDTH

            self.direction = 0
            self.hold_time = 0.0
            self.step_timer = 0.0  # Zeit bis zum nächsten Tile

            self.rect = pygame.Rect(
                0,
                self.y,
                PIXEL_WIDTH,
                PIXEL_WIDTH,
            )

        def update(self, dt):
            if self.direction == 0:
                self.hold_time = 0.0
                self.step_timer = 0.0
                return

            self.hold_time += dt

            accel = min(self.hold_time / ACCEL_TIME, 1.0)
            speed_multiplier = 1.0 + accel * (MAX_SPEED_MULTIPLIER - 1.0)

            # Tiles pro Sekunde
            tiles_per_second = BASE_SPEED * speed_multiplier
            seconds_per_tile = 1.0 / tiles_per_second

            self.step_timer += dt

            while self.step_timer >= seconds_per_tile:
                self.step_timer -= seconds_per_tile
                self.tile_x += self.direction

                self.tile_x = max(
                    0,
                    min(self.tile_x, MAP_WIDTH - 1)
                )

        @property
        def world_x(self):
            return self.tile_x * PIXEL_WIDTH

    player = Player()

    # -----------------------------
    # GAME LOOP
    # -----------------------------
    run = True
    while run:
        dt = clock.tick(60) / 1000.0

        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        # -----------------------------
        # INPUT (kontinuierlich!)
        # -----------------------------
        if inputs.LEFT in input_handler.pressed:
            player.direction = -1
        elif inputs.RIGHT in input_handler.pressed:
            player.direction = 1
        else:
            player.direction = 0

        # -----------------------------
        # UPDATE
        # -----------------------------
        player.update(dt)

        # -----------------------------
        # CAMERA
        # -----------------------------
        player_screen_x = player.world_x - camera_x
        if player_screen_x > SCROLL_BORDER:
            camera_x = player.world_x - SCROLL_BORDER

        camera_x = max(0, min(camera_x, WORLD_PIXEL_WIDTH - SCREEN_WIDTH))

        # -----------------------------
        # RENDER
        # -----------------------------
        screen.fill("black")

        for y, row in enumerate(world_map):
            for x, tile_id in enumerate(row):
                color = palette[tile_id]
                world_x = x * PIXEL_WIDTH
                screen_x = world_x - camera_x

                if -PIXEL_WIDTH <= screen_x <= SCREEN_WIDTH:
                    pygame.draw.rect(
                        screen,
                        color,
                        pygame.Rect(
                            screen_x,
                            y * PIXEL_WIDTH,
                            PIXEL_WIDTH,
                            PIXEL_WIDTH,
                        ),
                    )

        player.rect.x = player.world_x - camera_x
        player.rect.y = player.y

        draw_shaded_block(
            screen,
            player.rect,
            (255, 120, 120),
            (200, 0, 0),
            (120, 0, 0),
        )

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()
