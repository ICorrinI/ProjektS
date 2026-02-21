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
DJ_InputDelay = 0.03
GROUND_HEIGHT = 4 * PIXEL_WIDTH

# Dino
DINO_WIDTH  = 5 * PIXEL_WIDTH
DINO_HEIGHT = 5 * PIXEL_WIDTH
DINO_X = 6 * PIXEL_WIDTH
DINO_GRAVITY = 1
DINO_JUMP_FORCE = 25
CACTUS_WIDTH = 2 * PIXEL_WIDTH
CACTUS_MIN_HEIGHT = 3 * PIXEL_WIDTH
CACTUS_MAX_HEIGHT = 7 * PIXEL_WIDTH
CACTUS_MIN_DISTANCE = 1 * PIXEL_WIDTH
CACTUS_MAX_DISTANCE = 30 * PIXEL_WIDTH
GAME_SPEED = PIXEL_WIDTH
DINO_FPS = 30

# Tetris
TETRIS_CELL = BLOCK_SIZE
TETRIS_COLS = 10
TETRIS_OFFSET_Y = 0
TETRIS_ROWS = (SCREEN_HEIGHT - TETRIS_OFFSET_Y) // TETRIS_CELL
TETRIS_OFFSET_X = (SCREEN_WIDTH - (TETRIS_COLS * TETRIS_CELL)) // 2

SCORE_POSITION_X_TETRIS = TETRIS_OFFSET_X - 5 * PIXEL_WIDTH  
SCORE_POSITION_Y_TETRIS = BLOCK_SIZE

TETRIS_NEXT_SIZE = TETRIS_CELL // 2
TETRIS_NEXT_SPACING = 10
TETRIS_NEXT_OFFSET_X = TETRIS_OFFSET_X + TETRIS_COLS * TETRIS_CELL + 20
TETRIS_NEXT_OFFSET_Y = 120
TETRIS_NEXT_SLOT_HEIGHT = 4

TETRIS_HOLD_OFFSET_X = TETRIS_NEXT_OFFSET_X
TETRIS_HOLD_OFFSET_Y = TETRIS_NEXT_OFFSET_Y - (TETRIS_NEXT_SLOT_HEIGHT * TETRIS_NEXT_SIZE + 20)

TETRIS_FALL_SPEED = 30

# Mario
MARIO_WORLD = "Mario/1.json"
LEFT_SCROLL_BORDER = SCREEN_WIDTH * 0.4
RIGHT_SCROLL_BORDER = SCREEN_WIDTH * 0.6

BASE_SPEED = 1          
MAX_SPEED_MULTIPLIER = 2
ACCEL_TIME = 5

MOVE_INPUT_DELAY = 0.01

# Mario Spawn-Marker (Tile-Nummer, die als Spawnpunkt fungiert - gilt für alle Maps und Parts)
MAP_SPAWN_MARKER = 9

# Mario Finish-Marker (Tile-Nummer, die das Ende eines Parts markiert)
MAP_FINISH_MARKER = 10

GRAVITY = 50 * PIXEL_WIDTH              
JUMP_VELOCITY = 35 * PIXEL_WIDTH        
MAX_FALL_SPEED = 1000
INPUT_DELAY = 0.03

PIXEL_WIDTH = 20
SCREEN_WIDTH = 32 * PIXEL_WIDTH
SCREEN_HEIGHT = 32 * PIXEL_WIDTH

# --- TicTacToe Layout ---
TTT_CELL_SIZE = 10 * PIXEL_WIDTH
TTT_MARK_SIZE = 8 * PIXEL_WIDTH

# FX
TTT_CONFETTI_COUNT = 120
TTT_BOOM_COUNT = 160

# --- TicTacToe Icons (8x8, matrix clean) ---
TTT_X_ICON = [
    [1,0,0,0,0,0,0,1],
    [0,1,0,0,0,0,1,0],
    [0,0,1,0,0,1,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0],
    [0,0,1,0,0,1,0,0],
    [0,1,0,0,0,0,1,0],
    [1,0,0,0,0,0,0,1],
]

TTT_O_ICON = [
    [0,1,1,1,1,1,1,0],
    [1,1,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,1],
    [1,1,0,0,0,0,1,1],
    [0,1,1,1,1,1,1,0],
]

# --- Reaction Runner ---
RR_GRID = 32

RR_LANE_CENTERS = [8, 16, 24]
RR_LANE_START = 1
RR_LANE_SEP_1 = 12
RR_LANE_SEP_2 = 20

RR_PLAYER_SPRITE = [
    [0, 1, 1, 1, 0],
    [1, 2, 2, 2, 1],
    [1, 1, 1, 1, 1],
    [3, 0, 0, 0, 3],
]

RR_OBS_W = 2
RR_OBS_H = 2

RR_BASE_SPEED = 7.0
RR_SPEED_GAIN = 0.55
RR_BASE_SPAWN = 0.85
RR_MIN_SPAWN  = 0.28

RR_LEVEL_SECONDS = 6
RR_SPAWN_DECAY_PER_LEVEL = 0.06
RR_PLAYER_LANE_SPAWN_CHANCE = 0.20

# Hitbox smaller than sprite
RR_HITBOX_INSET_X = 1
RR_HITBOX_INSET_Y = 1
RR_HITBOX_SHRINK_W = 2
RR_HITBOX_SHRINK_H = 2

# Score position (grid coords!)
RR_SCORE_X = 1
RR_SCORE_Y = 1

# Game over behavior
RR_SHOW_SCORE_ON_GAME_OVER = True
RR_GAMEOVER_SCORE_X = 12
RR_GAMEOVER_SCORE_Y = 17

# Minimal digit font (3x5)
RR_FONT_3X5 = {
    "0": [[1,1,1],[1,0,1],[1,0,1],[1,0,1],[1,1,1]],
    "1": [[0,1,0],[1,1,0],[0,1,0],[0,1,0],[1,1,1]],
    "2": [[1,1,1],[0,0,1],[1,1,1],[1,0,0],[1,1,1]],
    "3": [[1,1,1],[0,0,1],[1,1,1],[0,0,1],[1,1,1]],
    "4": [[1,0,1],[1,0,1],[1,1,1],[0,0,1],[0,0,1]],
    "5": [[1,1,1],[1,0,0],[1,1,1],[0,0,1],[1,1,1]],
    "6": [[1,1,1],[1,0,0],[1,1,1],[1,0,1],[1,1,1]],
    "7": [[1,1,1],[0,0,1],[0,1,0],[0,1,0],[0,1,0]],
    "8": [[1,1,1],[1,0,1],[1,1,1],[1,0,1],[1,1,1]],
    "9": [[1,1,1],[1,0,1],[1,1,1],[0,0,1],[1,1,1]],
    " ": [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]],
}

# -------------------------
# Stack
# -------------------------
STACK_GRID = 32
STACK_FPS = 30

STACK_START_WIDTH = 10

# Geschwindigkeit in "cells per second"
STACK_BASE_SPEED = 10.0
STACK_SPEED_GAIN = 0.35
STACK_MAX_SPEED = 22.0

# Score Position (in GRID coords)
STACK_SCORE_X = 1
STACK_SCORE_Y = 1

# Subtile Guide-Linien (Grid-x Positionen)
STACK_GUIDE_XS = [8, 16, 24]   # zwei Guides, optional

# --- Memory Flash ---
MF_GRID_N = 3
MF_CELL = 10 * PIXEL_WIDTH          # 3*10 = 30 Matrix-Pixel -> passt perfekt in 32
MF_START_DELAY_MS = 450             # kurze Pause vor dem Abspielen
MF_FLASH_ON_MS = 380
MF_FLASH_OFF_MS = 180
MF_FAIL_MS = 700