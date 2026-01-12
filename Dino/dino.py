import pygame, random
from Settings.output import (
    draw_matrix,
    draw_matrix_representation,
    draw_score,
    draw_tiled_block
)
import Settings.settings as s
import Settings.colors as fc
from Settings.icons import draw_game_dino


def dino_game(screen, matrix, offset_canvas, started_on_pi):
    clock = pygame.time.Clock()

    def draw_cactus_branch(screen, trunk_x, trunk_width, y, side):
        length = 2 * s.PIXEL_WIDTH   
        thickness = s.PIXEL_WIDTH   
        yup = y - s.PIXEL_WIDTH

        if side == "left":
            bx = trunk_x - length
            bupx = bx 

        else:
            bx = trunk_x + trunk_width
            bupx = bx + s.PIXEL_WIDTH

        branch_rect = pygame.Rect(
            bx,
            y,
            length,        
            thickness      
        )   
        branch_up_rect = pygame.Rect(
            bupx,
            yup,
            thickness,       
            thickness      
        )
        pygame.draw.rect(screen, fc.DINO_BASE, branch_rect)
        pygame.draw.rect(screen, fc.DINO_DARK, branch_up_rect)

    # ---------------- PLAYER ----------------
    class Dino:
        def __init__(self):
            self.w = s.DINO_WIDTH
            self.h = s.DINO_HEIGHT
            self.x = s.DINO_X
            self.y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            self.vy = 0
            self.on_ground = True

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
            draw_game_dino(
                screen,
                int(self.x),
                int(self.y)
            )

    # ---------------- CACTUS ----------------
    class Cactus:
        def __init__(self):
            self.w = s.CACTUS_WIDTH
            self.segments = random.randint(1, 3)
            self.has_branch = random.choice([True, False])
            if self.has_branch and self.segments >= 2:
                self.branch_side = random.choice(["left", "right"])
                self.branch_height = random.randint(0, self.segments - 2)
            else:
                self.branch_side = None
            self.h = self.segments * s.BLOCK_SIZE
            self.x = s.SCREEN_WIDTH
            self.y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            self.passed = False

        def rect(self):
            return pygame.Rect(self.x, self.y, self.w, self.h)

        def update(self, speed):
            self.x -= speed

        def draw(self):
            # Stamm
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
            # Ast
            if self.branch_side is not None:
                branch_y = self.y + (self.segments - 1 - self.branch_height) * s.BLOCK_SIZE

                draw_cactus_branch(
                    screen,
                    self.x,
                    self.w,
                    branch_y,
                    self.branch_side
                )
        def get_branch_rects(self):
            rects = []

            if self.branch_side is None:
                return rects

            length = 2 * s.PIXEL_WIDTH
            thickness = s.PIXEL_WIDTH

            y = self.y + (self.segments - 1 - self.branch_height) * s.BLOCK_SIZE
            yup = y - s.PIXEL_WIDTH

            if self.branch_side == "left":
                bx = self.x - length
                bupx = bx
            else:
                bx = self.x + self.w
                bupx = bx + s.PIXEL_WIDTH

            rects.append(
                pygame.Rect(bx, y, length, thickness)
            )

            rects.append(
                pygame.Rect(bupx, yup, thickness, thickness)
            )

            return rects

    


    # ---------------- RESET ----------------
    def reset():
        return Dino(), [], 0, False, s.GAME_SPEED / 2

    while True:
        dino, obstacles, score, game_over, game_speed = reset()
        MAX_CACTI = 3

        while len(obstacles) < MAX_CACTI:
            if not obstacles:
                obstacles.append(Cactus())
            else:
                last = obstacles[-1]
                dist = random.randint(s.CACTUS_MIN_DISTANCE, s.CACTUS_MAX_DISTANCE)
                c = Cactus()
                c.x = last.x + last.w + dist
                obstacles.append(c)

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
                    obs.update(game_speed)

                    # Stamm-Kollision
                    if obs.rect().colliderect(dino.rect()):
                        game_over = True

                    # Ast-Kollision
                    for branch_rect in obs.get_branch_rects():
                        if branch_rect.colliderect(dino.rect()):
                            game_over = True

                    # SCORE + SPEED
                    if not obs.passed and obs.x + obs.w < dino.x:
                        obs.passed = True
                        score += 1

                        if score % 5 == 0:
                            game_speed += s.PIXEL_WIDTH / 4 

                        last = obstacles[-1]
                        dist = random.randint(s.CACTUS_MIN_DISTANCE, s.CACTUS_MAX_DISTANCE)
                        c = Cactus()
                        c.x = last.x + last.w + dist
                        obstacles.append(c)

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

            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                pygame.display.update()

            clock.tick(s.DINO_FPS)
