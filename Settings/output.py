import pygame
import Settings.colors as c
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
# Slightly optimized to perfrom less drawing operations
def draw_score(screen, number):
    if number > 99:
        number = 99# Overflow
    number_left = number // 10# Get tens place
    number_right = number - (number_left * 10)# Get ones place
    
    for i in range(5):
        for j in range(3):
            left_pos_x = s.SCORE_POSITION_X + (j * s.PIXEL_WIDTH)
            right_pos_x = left_pos_x + (5 * s.PIXEL_WIDTH)
            pos_y = s.SCORE_POSITION_Y + (i * s.PIXEL_WIDTH)
            if(score.SCORE[number_left][i][j]):
                pygame.draw.rect(screen, c.WHITE, (left_pos_x, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Left Number
            if(score.SCORE[number_right][i][j]):
                pygame.draw.rect(screen, c.WHITE, (right_pos_x, pos_y, s.PIXEL_WIDTH, s.PIXEL_WIDTH))# Right Number

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
