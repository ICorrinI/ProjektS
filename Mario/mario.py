import pygame
import json
import time
from Settings.icons import draw_icon_mario_mini
from Settings.output import draw_matrix_representation, draw_matrix, draw_shaded_block, draw_score
from Settings.colors import *
from Settings.settings import *
from Settings import inputs

def render_output(screen, started_on_pi, matrix, offset_canvas):
    """Unified render output for both Pi matrix and PC display"""
    if started_on_pi:
        return draw_matrix(screen, matrix, offset_canvas)
    else:
        draw_matrix_representation(screen)
        pygame.display.update()
        return offset_canvas

def update_camera(player_x, camera_x, WORLD_PIXEL_WIDTH):
    """Updates camera position based on player position"""
    player_screen_x = player_x - camera_x
    if player_screen_x > RIGHT_SCROLL_BORDER:
        camera_x += player_screen_x - RIGHT_SCROLL_BORDER
    elif player_screen_x < LEFT_SCROLL_BORDER:
        camera_x -= LEFT_SCROLL_BORDER - player_screen_x
    return max(0, min(camera_x, WORLD_PIXEL_WIDTH - SCREEN_WIDTH))

def calculate_tile_bounds(rect, PIXEL_WIDTH):
    """Calculate tile boundaries from a rect"""
    left_tile = int(rect.left // PIXEL_WIDTH)
    right_tile = int((rect.right - 1) // PIXEL_WIDTH)
    top_tile = int(rect.top // PIXEL_WIDTH)
    bottom_tile = int((rect.bottom - 1) // PIXEL_WIDTH)
    return left_tile, right_tile, top_tile, bottom_tile

def load_part(world_data, part_name):
    """
    Lädt einen Part aus den World-Daten und findet die Spawn-Position
    Gibt: (world_map, palette, spawn_tile_x, spawn_tile_y) zurück
    """
    part = world_data["parts"][part_name]
    world_map = part["map"]
    palette = {int(k): tuple(v) for k, v in part["palette"].items()}
    
    spawn_tile_x = 0
    spawn_tile_y = 0
    
    for y, row in enumerate(world_map):
        for x, tile in enumerate(row):
            if tile == MAP_SPAWN_MARKER:
                spawn_tile_x = x
                spawn_tile_y = y
                break
    
    return world_map, palette, spawn_tile_x, spawn_tile_y

def draw_pixel_number_mario(screen,number, center_x, center_y, selected):
    """Zeichnet Pixel-Zahlen für Map-Auswahl (1 oder 2)"""
    size =  BLOCK_SIZE

    # Farben für Map-Auswahl
    if number == 1:  # Rot für Map 1
        color_light = RED if selected else (80, 80, 80)
        color_base  = ORANGE if selected else (50, 50, 50)
        color_dark  = DARK_RED if selected else (30, 30, 30)
    elif number == 2:  # Blau für Map 2
        color_light = LIGHT_BLUE if selected else (80, 80, 80)
        color_base  = BLUE if selected else (50, 50, 50)
        color_dark  = DARK_BLUE if selected else (30, 30, 30)

    # 5x3 Pixel-Muster
    numbers = {
        1: [
            "010",
            "110",
            "010",
            "010",
            "111"
        ],
        2: [
            "111",
            "001",
            "111",
            "100",
            "111"
        ]
    }

    pattern = numbers[number]

    start_x = center_x - (len(pattern[0]) * size) // 2
    start_y = center_y - (len(pattern) * size) // 2

    for row_i, row in enumerate(pattern):
        for col_i, cell in enumerate(row):
            if cell == "1":
                rect = pygame.Rect(
                    start_x + col_i * size,
                    start_y + row_i * size,
                    size,
                    size
                )
                draw_shaded_block(screen, rect, color_light, color_base, color_dark)

def show_map_selection(screen, started_on_pi, matrix, offset_canvas, input_handler, clock):
    """Zeigt Map-Auswahl Screen (1 oder 2)"""
    selected_map = 0  # 0 = Map 1, 1 = Map 2
    choosing_map = True

    while choosing_map:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return None  # Zurück zum Menü

        if input_handler.is_pressed(inputs.UP):
            selected_map = 0
        elif input_handler.is_pressed(inputs.DOWN):
            selected_map = 1

        if input_handler.is_pressed(inputs.CONFIRM):
            choosing_map = False

        screen.fill("black")
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        draw_pixel_number_mario(screen, 1, center_x, center_y - 4 * BLOCK_SIZE, selected_map == 0)
        draw_pixel_number_mario(screen, 2, center_x, center_y + 4 * BLOCK_SIZE, selected_map == 1)

        offset_canvas = render_output(screen, started_on_pi, matrix, offset_canvas)
        clock.tick(15)

    # Rückgabe: Map-Dateiname (1.json oder 2.json)
    return "1.json" if selected_map == 0 else "2.json"

def show_final_score(screen, started_on_pi, matrix, offset_canvas, elapsed_time, input_handler):
    """
    Zeigt die Gesamtzeit am Ende aller Parts an
    Sperrt Input für 3 Sekunden, dann kann neu gestartet werden
    """
    # Zeit in Sekunden umrechnen und auf 0-9999 limit
    total_seconds = int(elapsed_time)
    display_time = total_seconds % 10000  # Für draw_score limitiert auf 0-9999
    
    clock = pygame.time.Clock()
    lock_time = 3.0  # 3 Sekunden Input-Lock
    elapsed_lock_time = 0.0
    
    wait_for_restart = True
    while wait_for_restart:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()
        input_handler.process_events(events)
        
        # Zähle Lock-Zeit nach oben
        if elapsed_lock_time < lock_time:
            elapsed_lock_time += dt
        
        # RENDER
        draw_score(screen, display_time)
        offset_canvas = render_output(screen, started_on_pi, matrix, offset_canvas)
        
        # Input nur akzeptieren nach 3 Sekunden Lock-Zeit
        if elapsed_lock_time >= lock_time:
            if input_handler.is_pressed(inputs.CONFIRM) or input_handler.is_pressed(inputs.LEFT) or input_handler.is_pressed(inputs.RIGHT):
                wait_for_restart = False
    
    return offset_canvas

def mario_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()

# Äußere Schleife für komplette Spiel-Sessions
    session_running = True
    while session_running:
        # Map-Auswahl anzeigen
        selected_mario_world = show_map_selection(screen, started_on_pi, matrix, offset_canvas, input_handler, clock)
        if selected_mario_world is None:
            return  # Zurück zum Hauptmenü

        # Innere Schleife für Game-Neustart nach Level-Ende
        game_running = True
        while game_running:
            # Start-Zeit für diese Spielrunde messen
            start_time = time.time()

            # Load World Map
            map_path = f"Mario/{selected_mario_world}"
            try:
                with open(map_path, "r") as f:
                    world_data = json.load(f)
            except FileNotFoundError:
                print(f"Fehler: {map_path} nicht gefunden!")
                game_running = False
                break

            # Alle verfügbaren Parts auflisten
            available_parts = list(world_data["parts"].keys())
            current_part_index = 0
            part_name = available_parts[current_part_index]

            world_map, palette, spawn_tile_x, spawn_tile_y = load_part(world_data, part_name)

            MAP_WIDTH = len(world_map[0])
            WORLD_PIXEL_WIDTH = MAP_WIDTH * PIXEL_WIDTH
            camera_x = 0
            DEATH_Y = 32 * PIXEL_WIDTH

            # Player Class and Instance
            class Player:
                def __init__(self, spawn_x, spawn_y):
                    self.w = 2 * PIXEL_WIDTH
                    self.h = 3 * PIXEL_WIDTH
                    self.spawn_tile_x = spawn_x
                    self.spawn_tile_y = spawn_y
                    self.coyote_time = 0  # Frames, in denen noch gespungen kann nach Boden-Verlust
                    self.reset()

                def reset(self):
                    self.x = self.spawn_tile_x * PIXEL_WIDTH
                    self.y = self.spawn_tile_y * PIXEL_WIDTH
                    self.tile_x = self.spawn_tile_x
                    self.tile_y = self.spawn_tile_y
                    self.vy = 0
                    self.on_ground = False
                    self.coyote_time = 0
                    self.direction = 0
                    self.hold_time = 0.0
                    self.speed_multiplier = 1.0

                def update(self, dt, world_map, physical_direction, step_triggered):
                    # Handle acceleration based on hold time
                    if physical_direction != 0:
                        self.direction = physical_direction
                        self.hold_time += dt
                        progress = min(self.hold_time / ACCEL_TIME, 1.0)
                        self.speed_multiplier = BASE_SPEED * (1 + progress * (MAX_SPEED_MULTIPLIER - 1))
                    else:
                        self.direction = 0
                        self.hold_time = 0.0
                        self.speed_multiplier = BASE_SPEED

                    # Horizontal movement
                    if step_triggered and self.direction != 0:
                        steps = int(self.speed_multiplier)
                        for _ in range(steps):
                            next_tile_x = self.tile_x + self.direction
                            collision = False
                            for dy in range(self.h // PIXEL_WIDTH):
                                check_x = next_tile_x + (0 if self.direction < 0 else (self.w // PIXEL_WIDTH - 1))
                                check_y = self.tile_y + dy
                                if 0 <= check_x < len(world_map[0]) and 0 <= check_y < len(world_map):
                                    tile = world_map[check_y][check_x]
                                    if tile != 0 and tile not in (MAP_SPAWN_MARKER, MAP_FINISH_MARKER, 12, 13):  # Kollision mit Block (außer Spawn/Finish)
                                        collision = True
                                        break
                            if not collision:
                                self.tile_x = next_tile_x
                                self.x = self.tile_x * PIXEL_WIDTH
                            else:
                                break

                    self.vy += GRAVITY * dt
                    new_y = self.y + self.vy * dt

                    if new_y >= DEATH_Y:
                        self.reset()
                        return

                    if new_y < 0:
                        new_y = 0
                        self.vy = 0

                    future_rect = pygame.Rect(self.x, new_y, self.w, self.h)
                    left_tile, right_tile, top_tile, bottom_tile = calculate_tile_bounds(future_rect, PIXEL_WIDTH)

                    self.on_ground = False
                    collision_detected = False

                    if self.vy >= 0:  # Falling
                        for tx in range(max(0, left_tile), min(len(world_map[0]), right_tile + 1)):
                            if 0 <= bottom_tile < len(world_map):
                                tile = world_map[bottom_tile][tx]
                                if tile != 0 and tile not in (MAP_SPAWN_MARKER, MAP_FINISH_MARKER, 12, 13):
                                    new_y = bottom_tile * PIXEL_WIDTH - self.h
                                    self.vy = 0
                                    self.on_ground = True
                                    self.coyote_time = 2
                                    collision_detected = True
                                    break
                    
                    if not self.on_ground and self.coyote_time > 0:
                        self.coyote_time -= 1
                    
                    if not collision_detected and self.vy < 0:  # Jumping
                        for tx in range(max(0, left_tile), min(len(world_map[0]), right_tile + 1)):
                            if top_tile >= 0:
                                tile = world_map[top_tile][tx]
                                if tile != 0 and tile not in (MAP_SPAWN_MARKER, MAP_FINISH_MARKER, 12, 13):
                                    new_y = (top_tile + 1) * PIXEL_WIDTH
                                    self.vy = 0
                                    collision_detected = True
                                    break

                    self.y = new_y
                    self.tile_y = int(self.y // PIXEL_WIDTH)

                def jump(self):
                    if self.on_ground or self.coyote_time > 0:
                        self.vy = -JUMP_VELOCITY
                        self.on_ground = False
                        self.coyote_time = 0

                def draw(self, screen, camera_x):
                    draw_icon_mario_mini(screen, int(self.x - camera_x), int(self.y))
                
                def check_finish_collision(self, world_map):
                    player_rect = pygame.Rect(self.x, self.y, self.w, self.h)
                    left_tile, right_tile, top_tile, bottom_tile = calculate_tile_bounds(player_rect, PIXEL_WIDTH)
                    
                    for ty in range(max(0, top_tile), min(len(world_map), bottom_tile + 1)):
                        for tx in range(max(0, left_tile), min(len(world_map[0]), right_tile + 1)):
                            if world_map[ty][tx] == MAP_FINISH_MARKER:
                                return True
                    return False

            player = Player(spawn_tile_x, spawn_tile_y)
            just_finished_part = False

            # Game Loop
            run = True
            while run:
                dt = clock.tick(60) / 1000.0
                events = pygame.event.get()
                input_handler.process_events(events)

                # Physical direction (continuous hold)
                physical_direction = 0
                if inputs.LEFT in input_handler.pressed:
                    physical_direction = -1
                elif inputs.RIGHT in input_handler.pressed:
                    physical_direction = 1

                # Back button check
                if input_handler.is_pressed_custom(inputs.BACK, INPUT_DELAY):
                    return
                
                # Step triggered (with delay)
                step_triggered = input_handler.is_pressed_custom(inputs.LEFT, INPUT_DELAY) or input_handler.is_pressed_custom(inputs.RIGHT, INPUT_DELAY)

                # Jump triggered (with delay)
                jump_triggered = input_handler.is_pressed_custom(inputs.CONFIRM, INPUT_DELAY) or input_handler.is_pressed_custom(inputs.UP, INPUT_DELAY)

                player.update(dt, world_map, physical_direction, step_triggered)

                if jump_triggered:
                    player.jump()

                if step_triggered:
                    just_finished_part = False

                if not just_finished_part and player.check_finish_collision(world_map):
                    if current_part_index < len(available_parts) - 1:
                        current_part_index += 1
                        part_name = available_parts[current_part_index]
                        world_map, palette, spawn_tile_x, spawn_tile_y = load_part(world_data, part_name)
                        player.spawn_tile_x = spawn_tile_x
                        player.spawn_tile_y = spawn_tile_y
                        player.reset()
                        MAP_WIDTH = len(world_map[0])
                        WORLD_PIXEL_WIDTH = MAP_WIDTH * PIXEL_WIDTH
                        camera_x = 0
                        just_finished_part = True
                    else:
                        elapsed_time = time.time() - start_time
                        offset_canvas = show_final_score(screen, started_on_pi, matrix, offset_canvas, elapsed_time, input_handler)
                        run = False
                        game_running = False

                # Update Camera
                camera_x = update_camera(player.x, camera_x, WORLD_PIXEL_WIDTH)

                # Render World and Player
                screen.fill((0, 0, 0))
                for y, row in enumerate(world_map):
                    for x, tile_id in enumerate(row):
                        if tile_id == 0: continue
                        color = palette.get(tile_id, (255, 255, 255))
                        world_x = x * PIXEL_WIDTH
                        screen_x = world_x - camera_x
                        if -PIXEL_WIDTH <= screen_x <= SCREEN_WIDTH:
                            pygame.draw.rect(screen, color, pygame.Rect(screen_x, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH))

                player.draw(screen, camera_x)
                offset_canvas = render_output(screen, started_on_pi, matrix, offset_canvas)