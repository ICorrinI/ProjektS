from Snake.snake import snake_game
from DoodleJump.doodlejump import doodle_jump_game
from Tetris.tetris import tetris_game
from Dino.dino import dino_game
from Mario.mario import mario_game

from Settings.icons import (
    draw_icon_snake,
    draw_icon_doodle_jump,
    draw_icon_dino,
    draw_icon_poweroff,
    draw_icon_tetris,
    draw_icon_mario,
)

# Jedes Spiel = ein Dict
# Reihenfolge = Reihenfolge im Menü (seitenweise, 2x2)

GAMES = [
    {
        "id": "snake",
        "icon": draw_icon_snake,
        "run": snake_game,
        "enabled": True,
    },
    {
        "id": "doodle_jump",
        "icon": draw_icon_doodle_jump,
        "run": doodle_jump_game,
        "enabled": True,
    },
    {
        "id": "dino",
        "icon": draw_icon_dino,   # Dummy-Icon
        "run": dino_game,
        "enabled": True,
    },
    {
        "id": "poweroff",
        "icon": draw_icon_poweroff,
        "run": "EXIT",
        "enabled": True,
    },
    # --- Seite 2---
    {
        "id": "tetris",
        "icon": draw_icon_tetris,
        "run": tetris_game,
        "enabled": True,
    },
    {
        "id": "mario",
        "icon": draw_icon_mario,
        "run": mario_game,
        "enabled": True,
    },
]
