import pygame
import random
from Settings.output import draw_matrix, draw_matrix_representation, draw_score, draw_shaded_block, draw_tiled_block
import Settings.settings as s
import Settings.colors as fc
from Settings import inputs


def doodle_jump_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    clock = pygame.time.Clock()


    class Player:
        def __init__(self):
            self.w = s.DJ_PLAYER_WIDTH
            self.h = s.DJ_PLAYER_HEIGHT
            self.world_x = 0
            self.world_y = 0
            self.vy = 0
            self.dead = False

        def reset(self):
            self.world_x = (s.SCREEN_WIDTH - self.w) // 2
            self.world_y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h - (2 * s.PIXEL_WIDTH)
            self.vy = 0
            self.dead = False

        def rect_world(self):
            return pygame.Rect(int(self.world_x), int(self.world_y), self.w, self.h)

        def update(self, platforms, camera_y):
            # integrate gravity
            self.vy += s.DJ_GRAVITY
            prev_y = self.world_y
            prev_bottom = prev_y + self.h
            self.world_y += self.vy
            curr_bottom = self.world_y + self.h

            # only check landing if falling
            if self.vy > 0:
                for p in platforms:
                    plat_top = p.rect.y
                    plat_rect = p.rect
                    player_rect_after = pygame.Rect(int(self.world_x), int(self.world_y), self.w, self.h)
                    if (prev_bottom <= plat_top <= curr_bottom) and player_rect_after.colliderect(plat_rect):
                        # land
                        self.world_y = plat_top - self.h
                        self.vy = -s.DJ_JUMP_HEIGHT
                        break
            
            # simple floor
            min_y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            if self.world_y > min_y:
                self.world_y = min_y
                if self.vy > 0:
                    self.vy = -s.DJ_JUMP_HEIGHT

            # death if falls below world screen
            if self.world_y - camera_y > s.SCREEN_HEIGHT:
                self.dead = True

    class Platform:
        def __init__(self, x, y, width=None):
            width = width or s.DJ_PLATFORM_WIDTH
            self.rect = pygame.Rect(int(x), int(y), int(width), int(s.DJ_PLATFORM_HEIGHT))

        def draw_screen(self, camera_y):
            draw_tiled_block(screen, self.rect, camera_y, fc.DJ_PLATFORM_LIGHT, fc.DJ_PLATFORM_BASE, fc.DJ_PLATFORM_DARK)

    def spawn_initial_platforms(count=6, vertical_spacing=s.DJ_PLATFORM_SPACING):
        plats = []
        base_y = s.SCREEN_HEIGHT - s.BLOCK_SIZE * 2
        for i in range(count):
            x = random.randint(0, s.SCREEN_WIDTH - s.DJ_PLATFORM_WIDTH)
            y = base_y - i * vertical_spacing
            plats.append(Platform(x, y))
        return plats

    def can_place(candidate_rect, existing):
        pad = 8
        for p in existing:
            if candidate_rect.colliderect(p.rect.inflate(pad, pad)):
                return False
        return True

    def generate_platform_above(existing, top_world_y, score):
        vertical_spacing = random.randint(
            int(s.DJ_PLATFORM_SPACING - 0.2 * s.DJ_PLATFORM_SPACING),
            int(s.DJ_PLATFORM_SPACING + 0.15 * s.DJ_PLATFORM_SPACING)
        )
        new_y = top_world_y - vertical_spacing

        # 🔥 Plattform-Breite abhängig vom Score
        if score >= 50:
            platform_width = int(s.DJ_PLATFORM_WIDTH * 0.4)  # sehr klein
        elif score >= 30:
            platform_width = int(s.DJ_PLATFORM_WIDTH * 0.6)  # klein
        elif score >= 10:
            platform_width = int(s.DJ_PLATFORM_WIDTH * 0.8)  # leicht kleiner
        else:
            platform_width = s.DJ_PLATFORM_WIDTH  # normal

        for _ in range(50):
            x = random.randint(0, s.SCREEN_WIDTH - platform_width)
            cand = pygame.Rect(x, new_y, platform_width, s.DJ_PLATFORM_HEIGHT)
            if can_place(cand, existing):
                return Platform(x, new_y, platform_width)

        return Platform(random.randint(0, s.SCREEN_WIDTH - platform_width), new_y, platform_width)


    # --- main loop ---
    while True:
        # reset world state
        player = Player()
        player.reset()
        camera_y = 0
        floor_rect_world = pygame.Rect(0, s.SCREEN_HEIGHT - s.GROUND_HEIGHT, s.SCREEN_WIDTH, s.GROUND_HEIGHT)
        platforms = spawn_initial_platforms()
        platforms.sort(key=lambda p: p.rect.y)
        score = 0
        run = True

        while run:
            # process pygame events through InputHandler
            events = pygame.event.get()
            input_handler.process_events(events)

            # exit/back
            if input_handler.is_pressed(inputs.BACK):
                return

            # LEFT / RIGHT movement
            if input_handler.is_pressed_custom(inputs.LEFT, s.DJ_InputDelay):
                player.world_x -= s.PIXEL_WIDTH
            if input_handler.is_pressed_custom(inputs.RIGHT, s.DJ_InputDelay):
                player.world_x += s.PIXEL_WIDTH

            # clamp horizontal
            player.world_x = max(0, min(s.SCREEN_WIDTH - player.w, player.world_x))

            # update player physics and collisions
            player.update(platforms, camera_y)

            # camera: follow player up only
            screen_player_y = player.world_y - camera_y
            if screen_player_y < s.SCREEN_HEIGHT // 2:
                camera_y = player.world_y - (s.SCREEN_HEIGHT // 2)

            # remove & respawn platforms below screen
            new_platforms = []
            top_world_y = min((p.rect.y for p in platforms), default=player.world_y)
            for p in platforms:
                if p.rect.y - camera_y > s.SCREEN_HEIGHT:
                    score += 1
                    filtered = [q for q in platforms if q is not p]
                    new_platforms.append(generate_platform_above(filtered, top_world_y, score))
                else:
                    new_platforms.append(p)
            platforms = sorted(new_platforms, key=lambda p: p.rect.y)

            # render
            screen.fill(fc.BLACK)
            for i, p in enumerate(platforms):
                if i == 0:
                    continue
                p.draw_screen(camera_y)

            draw_tiled_block(screen, floor_rect_world, camera_y, fc.GROUND_BROWN_LIGHT, fc.GROUND_BROWN_BASE, fc.GROUND_BROWN_DARK)
            player_screen_rect = pygame.Rect(int(player.world_x), int(player.world_y - camera_y), player.w, player.h)
            draw_shaded_block(screen, player_screen_rect, fc.DJ_PLAYER_LIGHT, fc.DJ_PLAYER_BASE, fc.DJ_PLAYER_DARK)

            # death handling
            if player.dead:
                draw_score(screen, score)
                if started_on_pi:
                    offset_canvas = draw_matrix(screen, matrix, offset_canvas)
                else:
                    draw_matrix_representation(screen)
                    pygame.display.update()

                waiting = True
                while waiting:
                    events = pygame.event.get()
                    input_handler.process_events(events)
                    if input_handler.is_pressed(inputs.CONFIRM):
                        waiting = False
                        run = False
                    elif input_handler.is_pressed(inputs.BACK):
                        return
                    clock.tick(s.DJ_SPEED)
                continue

            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                pygame.display.update()

           # Dynamische Geschwindigkeit
            if score >= 10:
                current_speed = 40   # schneller
            else:
                current_speed = s.DJ_SPEED  # normal (30)

            clock.tick(current_speed)
