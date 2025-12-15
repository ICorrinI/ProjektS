# This file stores setting to be used in all modules.

# All variables that have anything to do with diplaying should be multiples of 20 to represent the actual pixels on the matrix
SCREEN_WIDTH = 640 # The screen has to be seen as 32 20x20 pixels
SCREEN_HEIGHT = 640
PIXEL_WIDTH = 20 # Single pixel
DOWNWARD_PIXEL_PULL_OFFSET = 5
BLOCK_SIZE = 40

# Startscreen
SCREEN_HALF = SCREEN_WIDTH // 2

# Score
SCORE_POSITION_Y = PIXEL_WIDTH # One Pixel down
SCORE_POSITION_X = (SCREEN_WIDTH // 2) - (4 * PIXEL_WIDTH)

# Snake
SNAKE_SPEED = 10 # tickrate

# Doodle Jump
DJ_PLAYER_WIDTH = 2 * PIXEL_WIDTH
DJ_PLAYER_HEIGHT = 2 * PIXEL_WIDTH
DJ_JUMP_HEIGHT = 50
DJ_GRAVITY = 2
DJ_PLATFORM_WIDTH = 5 * BLOCK_SIZE
DJ_PLATFORM_HEIGHT = 2 * PIXEL_WIDTH
DJ_PLATFORM_SPACING = 12 * PIXEL_WIDTH
DJ_SPEED = 30
GROUND_HEIGHT = 4 * PIXEL_WIDTH
