import pygame, random
from Settings.output import draw_matrix, draw_matrix_representation, draw_score, draw_shaded_block, draw_tiled_block
import Settings.settings as s
import Settings.colors as fc

def doodle_jump_game(screen, matrix, offset_canvas, started_on_pi):
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
            # start on top of ground in world coords (camera_y=0 => screen bottom)
            self.world_y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h - (2 * s.PIXEL_WIDTH)
            self.vy = 0
            self.dead = False

        def rect_world(self):
            return pygame.Rect(int(self.world_x), int(self.world_y), self.w, self.h)

        def update(self, platforms):
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
            
            # Einfacher Boden: Player darf nicht unter den Boden fallen
            min_y = s.SCREEN_HEIGHT - s.GROUND_HEIGHT - self.h
            if self.world_y > min_y:
                self.world_y = min_y
                if self.vy > 0:
                    self.vy = -s.DJ_JUMP_HEIGHT  # stoppt nur die Fallgeschwindigkeit, kein Sprung

            # death if falls below world screen (world_y > camera_y + SCREEN_HEIGHT) — handled in main loop
            # but mark as dead if too far
            if self.world_y - camera_y > s.SCREEN_HEIGHT:
                self.dead = True

    # --- Platform in world coords ---
    class Platform:
        def __init__(self, x, y, width=None):
            width = width or s.DJ_PLATFORM_WIDTH
            self.rect = pygame.Rect(int(x), int(y), int(width), int(s.DJ_PLATFORM_HEIGHT))

        def draw_screen(self, camera_y):
            draw_tiled_block(screen, self.rect, camera_y, fc.DJ_PLATFORM_LIGHT, fc.DJ_PLATFORM_BASE, fc.DJ_PLATFORM_DARK)

    # --- helpers for platform generation ---
    def spawn_initial_platforms(count=6, vertical_spacing=s.DJ_PLATFORM_SPACING):
        plats = []
        base_y = s.SCREEN_HEIGHT - s.BLOCK_SIZE * 2
        for i in range(count):
            x = random.randint(0, s.SCREEN_WIDTH - s.DJ_PLATFORM_WIDTH)
            y = base_y - i * vertical_spacing
            plats.append(Platform(x, y))
        return plats

    def can_place(candidate_rect, existing):
        # ensure candidate doesn't overlap existing (with small padding)
        pad = 8
        for p in existing:
            if candidate_rect.colliderect(p.rect.inflate(pad, pad)):
                return False
        return True

    def generate_platform_above(existing, top_world_y):
        """
        Generate platform *above* top_world_y (smaller y).
        top_world_y = smallest y (highest platform) in world coordinates.
        """
        vertical_spacing = random.randint(
            int(s.DJ_PLATFORM_SPACING - 0.2 * s.DJ_PLATFORM_SPACING),
            int(s.DJ_PLATFORM_SPACING + 0.15 * s.DJ_PLATFORM_SPACING)
        )
        new_y = top_world_y - vertical_spacing

        attempts = 50
        for _ in range(attempts):
            x = random.randint(0, s.SCREEN_WIDTH - s.DJ_PLATFORM_WIDTH)
            cand = pygame.Rect(x, new_y, s.DJ_PLATFORM_WIDTH, s.DJ_PLATFORM_HEIGHT)
            if can_place(cand, existing):
                return Platform(x, new_y)
        # fallback: place anyway at new_y
        return Platform(random.randint(0, s.SCREEN_WIDTH - s.DJ_PLATFORM_WIDTH), new_y)

    # --- main loop: outer loop restarts full game cleanly ---
    while True:
        # reset world state
        player = Player()
        player.reset()
        camera_y = 0  # world y coordinate at top of screen
        floor_rect_world = pygame.Rect(0, s.SCREEN_HEIGHT - s.GROUND_HEIGHT, s.SCREEN_WIDTH, s.GROUND_HEIGHT)

        platforms = spawn_initial_platforms()
        # ensure platforms sorted by y (ascending = higher up)
        platforms.sort(key=lambda p: p.rect.y)
        score = 0

        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        return

            # input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player.world_x -= s.PIXEL_WIDTH
            if keys[pygame.K_RIGHT]:
                player.world_x += s.PIXEL_WIDTH
            # clamp horizontal
            player.world_x = max(0, min(s.SCREEN_WIDTH - player.w, player.world_x))

            # update player physics and collisions (platforms are in world coords)
            player.update(platforms)

            # camera: follow player up only
            screen_player_y = player.world_y - camera_y
            if screen_player_y < s.SCREEN_HEIGHT // 2:
                camera_y = player.world_y - (s.SCREEN_HEIGHT // 2)

            # remove & respawn platforms that fell below screen (world_y - camera_y > SCREEN_HEIGHT)
            new_platforms = []
            top_world_y = min((p.rect.y for p in platforms), default=player.world_y)
            for p in platforms:
                if p.rect.y - camera_y > s.SCREEN_HEIGHT:
                    # platform is below screen, count it and spawn replacement above current top
                    score += 1
                    # generate replacement that doesn't collide with existing (excluding this p)
                    filtered = [q for q in platforms if q is not p]
                    new_p = generate_platform_above(filtered, top_world_y)
                    new_platforms.append(new_p)
                    # update top_world_y if new one is higher
                    if new_p.rect.y < top_world_y:
                        top_world_y = new_p.rect.y
                else:
                    new_platforms.append(p)

            platforms = new_platforms
            # ensure list is sorted by y ascending (top first)
            platforms.sort(key=lambda p: p.rect.y)

            screen.fill(fc.BLACK)

            # draw platforms (skip first visual if you want ground hidden — user asked earlier)
            for i, p in enumerate(platforms):
                if i == 0:
                    # still keep it for collisions, just don't draw it
                    continue
                p.draw_screen(camera_y)

            # draw floor (convert world to screen)
            draw_tiled_block(screen, floor_rect_world, camera_y, fc.GROUND_BROWN_LIGHT, fc.GROUND_BROWN_BASE, fc.GROUND_BROWN_DARK)

            # draw player at screen pos
            player_screen_rect = pygame.Rect(int(player.world_x), int(player.world_y - camera_y), player.w, player.h)
            draw_shaded_block(screen, player_screen_rect, fc.DJ_PLAYER_LIGHT, fc.DJ_PLAYER_BASE, fc.DJ_PLAYER_DARK)

            # death handling: if player below visible world bottom
            if player.world_y - camera_y > s.SCREEN_HEIGHT:
                # show score
                draw_score(screen, score)
                if started_on_pi:
                    offset_canvas = draw_matrix(screen, matrix, offset_canvas)
                else:
                    draw_matrix_representation(screen)
                    pygame.display.update()

                waiting = True
                while waiting:
                    for ev in pygame.event.get():
                        if ev.type == pygame.QUIT:
                            return
                        if ev.type == pygame.KEYDOWN:
                            waiting = False
                            run = False
                    clock.tick(s.DJ_SPEED)
                continue

            # output to matrix or window
            if started_on_pi:
                offset_canvas = draw_matrix(screen, matrix, offset_canvas)
            else:
                draw_matrix_representation(screen)
                pygame.display.update()

            clock.tick(s.DJ_SPEED)
