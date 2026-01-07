import pygame, random
from Settings.output import (
    draw_matrix,
    draw_matrix_representation,
    draw_score,
    draw_tiled_block
)
import Settings.settings as s
import Settings.colors as fc


def dino_game(screen, matrix, offset_canvas, started_on_pi):
    clock = pygame.time.Clock()

    # ---------------- PLAYER ----------------
    class Dino:
        def __init__(self):
            self.w = s.DINO_WIDTH
            self.h = s.DINO_HEIGHT
            self.x = s.DINO_X
            self.y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            self.vy = 0
            self.on_ground = True
            self.dead = False

        def rect(self):
            return pygame.Rect(self.x, self.y, self.w, self.h)

        def jump(self):
            if self.on_ground:
                self.vy = -s.DINO_JUMP_FORCE
                self.on_ground = False

        def update(self):
            self.vy += s.DINO_GRAVITY
            self.y += self.vy
            ground_y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            if self.y >= ground_y:
                self.y = ground_y
                self.vy = 0
                self.on_ground = True

        def draw(self):
            draw_tiled_block(screen, self.rect(), 0,
                              fc.DINO_LIGHT,
                              fc.DINO_BASE,
                              fc.DINO_DARK)

    # ---------------- OBSTACLE ----------------
    class Cactus:
        def __init__(self):
            self.w = s.CACTUS_WIDTH
            self.segments = random.randint(1, 3)
            self.h = self.segments * s.BLOCK_SIZE
            self.x = s.SCREEN_WIDTH
            self.y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            self.speed = s.GAME_SPEED / 2
            self.passed = False  

        def rect(self):
            return pygame.Rect(self.x, self.y, self.w, self.h)

        def update(self):
            self.x -= self.speed

        def draw(self):
            for i in range(self.segments):
                seg_rect = pygame.Rect(
                    self.x,
                    self.y + (self.segments - 1 - i) * s.BLOCK_SIZE,
                    self.w,
                    s.BLOCK_SIZE
                )
                draw_tiled_block(
                    screen,
                    seg_rect,
                    0,
                    fc.DINO_LIGHT,
                    fc.DINO_BASE,
                    fc.DINO_DARK
                )

    # ---------------- RESET ----------------
    def reset():
        return Dino(), [], 0, False

    while True:
        dino, obstacles, score, game_over = reset()
        MAX_CACTI = 3

        while len(obstacles) < MAX_CACTI:
            if len(obstacles) == 0:
                obstacles.append(Cactus())
            else:
                last = obstacles[-1]
                next_distance = random.randint(s.CACTUS_MIN_DISTANCE, s.CACTUS_MAX_DISTANCE)
                new_cactus = Cactus()
                new_cactus.x = last.x + last.w + next_distance
                obstacles.append(new_cactus)

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        dino.jump()
                    if game_over:
                        run = False

            if not game_over:
                dino.update()
                for obs in obstacles:
                    obs.update()

                    if obs.rect().colliderect(dino.rect()):
                        game_over = True

                    # -------- SCORE UND NEUER KAKTUS --------
                    if not obs.passed and obs.x + obs.w < dino.x:
                        obs.passed = True
                        score += 1

                       
                        last = obstacles[-1]
                        next_distance = random.randint(s.CACTUS_MIN_DISTANCE, s.CACTUS_MAX_DISTANCE)
                        new_cactus = Cactus()
                        new_cactus.x = last.x + last.w + next_distance
                        obstacles.append(new_cactus)

                obstacles = [o for o in obstacles if o.x + o.w > 0]

            screen.fill(fc.BLACK)


            ground_rect = pygame.Rect(
                0,
                s.SCREEN_HEIGHT - s.GROUND_HEIGHT,
                s.SCREEN_WIDTH,
                s.GROUND_HEIGHT
            )
            draw_tiled_block(
                screen,
                ground_rect,
                0,
                fc.DINO_LIGHT,
                fc.DINO_BASE,
                fc.DINO_DARK
            )

            dino.draw()
            for obs in obstacles:
                obs.draw()

            if game_over:
                draw_score(screen, score)

            # -------- MATRIX OUTPUT --------
            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                pygame.display.update()

            clock.tick(s.DINO_FPS)
