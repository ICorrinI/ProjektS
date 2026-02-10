import pygame
import random

from Settings.output import draw_matrix_representation, draw_matrix, draw_score, draw_shaded_block
from Settings.colors import *
from Settings.settings import SNAKE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE
from Settings import inputs

def snake_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()

    # -----------------------------
    # LEVEL AUSWAHL (Pixel-Version)
    # -----------------------------
    selected_level = 0   # 0 = Level 1, 1 = Level 2
    choosing_level = True

    # Hilfsfunktion: Pixel-Zahlen für Level-Auswahl zeichnen
    def draw_pixel_number(number, center_x, center_y, selected):
        size = BLOCK_SIZE

        # Farben für Level-Auswahl
        if number == 1:  # Grün für Level 1
            color_light = SNAKE_LIGHT if selected else (80, 80, 80)
            color_base  = SNAKE_BASE  if selected else (50, 50, 50)
            color_dark  = SNAKE_DARK  if selected else (30, 30, 30)
        elif number == 2:  # Blau für Level 2
            color_light = SNAKE2_LIGHT if selected else (80, 80, 80)
            color_base  = SNAKE2_BASE  if selected else (50, 50, 50)
            color_dark  = SNAKE2_DARK  if selected else (30, 30, 30)

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

    # -----------------------------
    # LEVEL AUSWAHL LOOP
    # -----------------------------
    while choosing_level:
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        if input_handler.is_pressed(inputs.UP):
            selected_level = 0
        elif input_handler.is_pressed(inputs.DOWN):
            selected_level = 1

        if input_handler.is_pressed(inputs.CONFIRM):
            choosing_level = False

        screen.fill("black")
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        draw_pixel_number(1, center_x, center_y - 4 * BLOCK_SIZE, selected_level == 0)
        draw_pixel_number(2, center_x, center_y + 4 * BLOCK_SIZE, selected_level == 1)

        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(15)

    # -----------------------------
    # Geschwindigkeit und Farben je nach Level
    # -----------------------------
    if selected_level == 0:  # Level 1
        game_speed = SNAKE_SPEED
        snake_light = SNAKE_LIGHT
        snake_base  = SNAKE_BASE
        snake_dark  = SNAKE_DARK
        apple_count = 1
    else:                    # Level 2
        game_speed = SNAKE_SPEED + 10
        snake_light = SNAKE2_LIGHT
        snake_base  = SNAKE2_BASE
        snake_dark  = SNAKE2_DARK
        apple_count = 2

    # -----------------------------
    # Snake-Klasse
    # -----------------------------
    class Snake:
        def __init__(self):
            self.reset()

        def reset(self):
            self.x = BLOCK_SIZE
            self.y = BLOCK_SIZE
            self.xdir = 1
            self.ydir = 0
            self.head = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
            self.body = [pygame.Rect(self.x - BLOCK_SIZE, self.y, BLOCK_SIZE, BLOCK_SIZE)]
            self.dead = False

        def update(self):
            # Shift body
            self.body.append(self.head.copy())
            for i in range(len(self.body) - 1):
                self.body[i].x, self.body[i].y = self.body[i + 1].x, self.body[i + 1].y
            self.body.pop()

            # Move head
            self.head.x += self.xdir * BLOCK_SIZE
            self.head.y += self.ydir * BLOCK_SIZE

            # Collision with walls
            if (
                self.head.x < 0
                or self.head.x >= SCREEN_WIDTH
                or self.head.y < 0
                or self.head.y >= SCREEN_HEIGHT
            ):
                self.dead = True

            # Collision with body
            for square in self.body:
                if self.head.x == square.x and self.head.y == square.y:
                    self.dead = True

    # -----------------------------
    # Apple-Klasse
    # -----------------------------
    class Apple:
        def __init__(self):
            self.respawn()

        def respawn(self):
            valid = False
            while not valid:
                self.x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
                self.y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE

                valid = True
                if self.x == snake.head.x and self.y == snake.head.y:
                    valid = False
                for sq in snake.body:
                    if self.x == sq.x and self.y == sq.y:
                        valid = False

            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

        def draw(self):
            draw_shaded_block(screen, self.rect, APPLE_LIGHT, APPLE_BASE, APPLE_DARK)

    # -----------------------------
    # Spielobjekte initialisieren
    # -----------------------------
    snake = Snake()
    apples = [Apple() for _ in range(apple_count)]
    score_value = 0

    # -----------------------------
    # Haupt-Game-Loop
    # -----------------------------
    run = True
    while run:
        # INPUT HANDLING
        events = pygame.event.get()
        input_handler.process_events(events)

        if input_handler.is_pressed(inputs.BACK):
            return

        if input_handler.is_pressed(inputs.LEFT) and snake.xdir != 1:
            snake.xdir = -1
            snake.ydir = 0
        elif input_handler.is_pressed(inputs.RIGHT) and snake.xdir != -1:
            snake.xdir = 1
            snake.ydir = 0
        elif input_handler.is_pressed(inputs.UP) and snake.ydir != 1:
            snake.xdir = 0
            snake.ydir = -1
        elif input_handler.is_pressed(inputs.DOWN) and snake.ydir != -1:
            snake.xdir = 0
            snake.ydir = 1

        # UPDATE GAME LOGIC
        snake.update()

        # Check apple collision
        for apple in apples:
            if snake.head.x == apple.x and snake.head.y == apple.y:
                snake.body.append(pygame.Rect(apple.x, apple.y, BLOCK_SIZE, BLOCK_SIZE))
                apple.respawn()
                score_value += 1

        # RENDER
        screen.fill("black")
        for apple in apples:
            apple.draw()
        draw_shaded_block(screen, snake.head, snake_light, snake_base, snake_dark)
        for sq in snake.body:
            draw_shaded_block(screen, sq, snake_light, snake_base, snake_dark)

        # Snake dead → score anzeigen + warten
        if snake.dead:
            draw_score(screen, score_value)
            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                pygame.display.update()

            wait_for_restart = True
            while wait_for_restart:
                events = pygame.event.get()
                input_handler.process_events(events)

                if input_handler.is_pressed(inputs.CONFIRM):
                    # Reset game
                    snake.reset()
                    for apple in apples:
                        apple.respawn()
                    score_value = 0
                    wait_for_restart = False
                elif input_handler.is_pressed(inputs.BACK):
                    return

                clock.tick(game_speed)
            continue

        # MATRIX OUTPUT
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(game_speed)
