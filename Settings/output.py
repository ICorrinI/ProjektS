import pygame
import Settings.colors as fc
import Settings.settings as s
import Settings.score as score
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    pass

def draw_matrix(screen, matrix, offset_canvas):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y + s.DOWNWARD_PIXEL_PULL_OFFSET))# get color in format (r, g, b, t)            
            offset_canvas.SetPixel(x, y, color[0], color[1], color[2])
    return matrix.SwapOnVSync(offset_canvas)

# This serves to represent how the game will actually look on the matrix in the window
def draw_matrix_representation(screen):
    for y in range(32):
        for x in range(32):
            pos_x = x * s.PIXEL_WIDTH
            pos_y = y * s.PIXEL_WIDTH
            color = screen.get_at((pos_x, pos_y + s.DOWNWARD_PIXEL_PULL_OFFSET))# get color in format (r, g, b, t)
            pygame.draw.rect(screen, color, (pos_x + s.SCREEN_WIDTH, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Single Pixel representation
    pygame.draw.rect(screen, (0, 0, 0), (s.SCREEN_WIDTH, 0, 1, s.SCREEN_HEIGHT))# Seperating line

# This draws the score on the screen
# Unterstützt jetzt auch Scores über 99 (flexibel erweitert, zentral positioniert)
def draw_score(screen, number):
    # Begrenzung für sehr große Zahlen
    if number > 9999999:
        number = 9999999
    
    # Konvertiere zu String um Anzahl der Ziffern zu bekommen
    score_str = str(number)
    num_digits = len(score_str)
    
    # Berechne die Gesamtbreite in Pixeln
    # Jede Ziffer: 3 Spalten breit, mit 1 Space Abstand zwischen Ziffern
    digit_pixel_width = 4 * s.PIXEL_WIDTH  # 3 Spalten + 1 Space
    total_pixel_width = num_digits * digit_pixel_width - s.PIXEL_WIDTH  # Letztes Space abziehen
    
    # Berechne Start-X Position für Zentrierung im Screen
    start_x = s.SCREEN_WIDTH // 2 - total_pixel_width // 2
    
    # Zeichne jede Ziffer
    for digit_idx, digit_char in enumerate(score_str):
        digit = int(digit_char)
        for i in range(5):  # 5 Reihen pro Ziffer
            for j in range(3):  # 3 Spalten pro Ziffer
                pos_x = start_x + digit_idx * digit_pixel_width + j * s.PIXEL_WIDTH
                pos_y = s.SCORE_POSITION_Y + i * s.PIXEL_WIDTH
                if score.SCORE[digit][i][j]:
                    pygame.draw.rect(screen, fc.WHITE, (pos_x, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))

def draw_score_tetris(screen, number):
    score_str = str(number)  # z.B. "10"
    for idx, digit_char in enumerate(score_str):
        digit = int(digit_char)
        for i in range(5):  # Zeilen des Ziffern-Arrays
            for j in range(3):  # Spalten des Ziffern-Arrays
                pos_x = s.SCORE_POSITION_X_TETRIS + j * s.PIXEL_WIDTH
                pos_y = s.SCORE_POSITION_Y_TETRIS + idx * 6 * s.PIXEL_WIDTH + i * s.PIXEL_WIDTH
                if score.SCORE[digit][i][j]:
                    pygame.draw.rect(screen, fc.WHITE, (pos_x, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))

# does shading for 4px Blocks
def draw_shaded_block(screen, rect, light, base, dark):
    bs = rect.width // 2

    # Quad 1 – oben links (hell)
    pygame.draw.rect(screen, light, (rect.x, rect.y, bs, bs))

    # Quad 2 – oben rechts (base)
    pygame.draw.rect(screen, base, (rect.x + bs, rect.y, bs, bs))

    # Quad 3 – unten links (base)
    pygame.draw.rect(screen, base, (rect.x, rect.y + bs, bs, bs))

    # Quad 4 – unten rechts (dunkel)
    pygame.draw.rect(screen, dark, (rect.x + bs, rect.y + bs, bs, bs))

def draw_tiled_block(screen, rect, camera_y, light, base, dark):
    BLOCK = s.BLOCK_SIZE
    screen_rect = pygame.Rect(rect.x, rect.y - camera_y, rect.width, rect.height)

    BLOCK_W = screen_rect.width // BLOCK
    BLOCK_H = screen_rect.height // BLOCK

    for by in range(BLOCK_H):
        for bx in range(BLOCK_W):
            cell = pygame.Rect(
                screen_rect.x + bx * BLOCK,
                screen_rect.y + by * BLOCK,
                BLOCK,
                BLOCK
            )
            draw_shaded_block(screen, cell, light, base, dark)

