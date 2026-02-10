import pygame
import json
from Settings.icons import draw_icon_mario_mini
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
    DEATH_Y = 32 * PIXEL_WIDTH

    # -----------------------------
    # PLAYER
    # -----------------------------
    class Player:
        def __init__(self):
            self.w = 2 * PIXEL_WIDTH
            self.h = 3 * PIXEL_WIDTH
            self.reset()

        def reset(self):
            self.tile_x = SPAWN_TILE_X
            self.tile_y = SPAWN_TILE_Y if SPAWN_TILE_Y is not None else MAP_HEIGHT - 1
            self.x = self.tile_x * PIXEL_WIDTH
            self.y = self.tile_y * PIXEL_WIDTH
            self.vy = 0
            self.on_ground = False

            self.direction = 0
            self.hold_time = 0.0
            self.speed_multiplier = 1.0

        def update(self, dt, world_map, physical_direction, step_triggered):
            # ---------------------------------
            # HOLD TIME läuft solange gedrückt
            # ---------------------------------
            if physical_direction != 0:
                self.direction = physical_direction
                self.hold_time += dt
                progress = min(self.hold_time / ACCEL_TIME, 1.0)
                self.speed_multiplier = BASE_SPEED * (1 + progress * (MAX_SPEED_MULTIPLIER - 1))
            else:
                self.direction = 0
                self.hold_time = 0.0
                self.speed_multiplier = BASE_SPEED

            print(f"Direction: {self.direction}, Hold Time: {self.hold_time:.2f}s, Speed Multiplier: {self.speed_multiplier:.2f}")

            # ---------------------------------
            # Bewegung nur bei Custom-Trigger
            # ---------------------------------
            if step_triggered and self.direction != 0:
                steps = int(self.speed_multiplier)

                for _ in range(steps):
                    next_tile_x = self.tile_x + self.direction
                    collision = False

                    for dy in range(self.h // PIXEL_WIDTH):
                        check_y = self.tile_y + dy
                        if 0 <= next_tile_x < len(world_map[0]) and check_y < len(world_map):
                            if world_map[check_y][next_tile_x] != 0:
                                collision = True
                                break

                    if not collision:
                        self.tile_x = next_tile_x
                        self.x = self.tile_x * PIXEL_WIDTH
                    else:
                        break

            # ---------------------------------
            # GRAVITY
            # ---------------------------------
            self.vy += GRAVITY * dt
            new_y = self.y + self.vy * dt

            if new_y >= DEATH_Y:
                self.reset()
                return

            future_rect = pygame.Rect(self.x, new_y, self.w, self.h)
            left_tile = int(future_rect.left // PIXEL_WIDTH)
            right_tile = int((future_rect.right - 1) // PIXEL_WIDTH)
            top_tile = int(future_rect.top // PIXEL_WIDTH)
            bottom_tile = int((future_rect.bottom - 1) // PIXEL_WIDTH)

            self.on_ground = False

            for tx in range(left_tile, right_tile + 1):
                if bottom_tile < len(world_map) and world_map[bottom_tile][tx] != 0:
                    new_y = bottom_tile * PIXEL_WIDTH - self.h
                    self.vy = 0
                    self.on_ground = True
                    break

            for tx in range(left_tile, right_tile + 1):
                if top_tile >= 0 and world_map[top_tile][tx] != 0:
                    new_y = (top_tile + 1) * PIXEL_WIDTH
                    self.vy = 0
                    break

            self.y = new_y
            self.tile_y = int(self.y // PIXEL_WIDTH)

        def jump(self):
            if self.on_ground:
                self.vy = -JUMP_VELOCITY
                self.on_ground = False

        def draw(self, camera_x):
            draw_icon_mario_mini(screen, int(self.x - camera_x), int(self.y))

    player = Player()

    # -----------------------------
    # GAME LOOP
    # -----------------------------
    run = True
    while run:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed_custom(inputs.BACK, INPUT_DELAY):
            return

        # ---------------------------------
        # PHYSICAL HOLD CHECK (kein Delay!)
        # ---------------------------------
        physical_direction = 0
        if inputs.LEFT in input_handler.pressed:
            physical_direction = -1
        elif inputs.RIGHT in input_handler.pressed:
            physical_direction = 1

        # ---------------------------------
        # CUSTOM STEP CHECK
        # ---------------------------------
        step_triggered = False
        if input_handler.is_pressed_custom(inputs.LEFT, INPUT_DELAY):
            step_triggered = True
        elif input_handler.is_pressed_custom(inputs.RIGHT, INPUT_DELAY):
            step_triggered = True

        if inputs.CONFIRM in input_handler.pressed or inputs.UP in input_handler.pressed:
            player.jump()

        player.update(dt, world_map, physical_direction, step_triggered)

        # ---------------------------------
        # CAMERA
        # ---------------------------------
        player_screen_x = player.x - camera_x
        left_scroll_border = SCREEN_WIDTH * 0.4
        right_scroll_border = SCREEN_WIDTH * 0.6

        if player_screen_x > right_scroll_border:
            camera_x += player_screen_x - right_scroll_border
        elif player_screen_x < left_scroll_border:
            camera_x -= left_scroll_border - player_screen_x

        camera_x = max(0, min(camera_x, WORLD_PIXEL_WIDTH - SCREEN_WIDTH))

        # ---------------------------------
        # RENDER
        # ---------------------------------
        screen.fill((0, 0, 0))
        for y, row in enumerate(world_map):
            for x, tile_id in enumerate(row):
                if tile_id == 0:
                    continue
                color = palette[tile_id]
                world_x = x * PIXEL_WIDTH
                screen_x = world_x - camera_x
                if -PIXEL_WIDTH <= screen_x <= SCREEN_WIDTH:
                    pygame.draw.rect(screen, color, pygame.Rect(screen_x, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH))

        player.draw(camera_x)

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

