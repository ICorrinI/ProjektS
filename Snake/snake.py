import pygame
from pygame.locals import *
import random
from Settings.output import draw_matrix_representation, draw_matrix, draw_score, draw_shaded_block
from Settings.colors import *
from Settings.settings import SNAKE_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE

started_on_pi = True
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    started_on_pi = False


def snake_game(screen, matrix, offset_canvas):
    clock = pygame.time.Clock()

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
            global apple

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

    class Apple:
        def __init__(self):
            self.respawn()

        def respawn(self):
            valid = False
            while not valid:
                self.x = random.randint(0, (SCREEN_WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE
                self.y = random.randint(0, (SCREEN_HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE

                # Check collision with snake
                valid = True
                if self.x == snake.head.x and self.y == snake.head.y:
                    valid = False
                for sq in snake.body:
                    if self.x == sq.x and self.y == sq.y:
                        valid = False

            self.rect = pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)

        def draw(self):
            draw_shaded_block(screen, self.rect, APPLE_LIGHT, APPLE_BASE, APPLE_DARK)

    snake = Snake()
    apple = Apple()

    score_value = 0
    event_thrown = False
    run = True

    while run:

        # INPUT -----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN and not event_thrown:
                if event.key == pygame.K_LEFT and snake.xdir != 1:
                    snake.xdir = -1
                    snake.ydir = 0
                    event_thrown = True
                elif event.key == pygame.K_RIGHT and snake.xdir != -1:
                    snake.xdir = 1
                    snake.ydir = 0
                    event_thrown = True
                elif event.key == pygame.K_UP and snake.ydir != 1:
                    snake.xdir = 0
                    snake.ydir = -1
                    event_thrown = True
                elif event.key == pygame.K_DOWN and snake.ydir != -1:
                    snake.xdir = 0
                    snake.ydir = 1
                    event_thrown = True
                elif event.key == pygame.K_s:
                    return

        event_thrown = False

        # UPDATE -----------------------------
        snake.update()

        # Check apple
        if snake.head.x == apple.x and snake.head.y == apple.y:
            snake.body.append(pygame.Rect(apple.x, apple.y, BLOCK_SIZE, BLOCK_SIZE))
            apple.respawn()
            score_value += 1

        # DRAW -------------------------------
        screen.fill("black")

        apple.draw()
        draw_shaded_block(screen, snake.head, SNAKE_LIGHT, SNAKE_BASE, SNAKE_DARK)
        for sq in snake.body:
            draw_shaded_block(screen, sq, SNAKE_LIGHT, SNAKE_BASE, SNAKE_DARK)

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
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        # Reset game
                        snake.reset()
                        apple.respawn()
                        score_value = 0
                        wait_for_restart = False
                    elif event.type == pygame.QUIT:
                        return

                clock.tick(SNAKE_SPEED)
            continue

        # MATRIX OUTPUT -----------------------
        if started_on_pi:
            offset_canvas = draw_matrix(screen, matrix, offset_canvas)
        else:
            draw_matrix_representation(screen)
            pygame.display.update()

        clock.tick(SNAKE_SPEED)
