from Snake.snake import snake_game
from DoodleJump.doodlejump import doodle_jump_game
from Tetris.tetris import tetris_game
from Dino.dino import dino_game
from Mario.mario import mario_game
from TicTacToe.tictactoe import tictactoe_game
from ReactionRunner.reactionrunner import reaction_runner_game
from Stack.stack import stack_game
from MemoryFlash.memoryflash import memory_flash_game

from Settings.icons import (
    draw_icon_snake,
    draw_icon_doodle_jump,
    draw_icon_dino,
    draw_icon_poweroff,
    draw_icon_tetris,
    draw_icon_mario,
    draw_icon_tictactoe,
    draw_icon_reaction_runner,
    draw_icon_stack,
    draw_icon_memory_flash
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
        "icon": draw_icon_dino,
        "run": dino_game,
        "enabled": True,
    },
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
    {
        "id": "tictactoe",
        "icon": draw_icon_tictactoe,
        "run": tictactoe_game,
        "enabled": True,
    },
    {
        "id": "reaction_runner",
        "icon": draw_icon_reaction_runner,
        "run": reaction_runner_game,
        "enabled": True,
    },
    {
        "id": "stack",
        "icon": draw_icon_stack,
        "run": stack_game,
        "enabled": True,       
    },
    {
        "id": "memory_flash",
        "icon": draw_icon_memory_flash,
        "run": memory_flash_game,
        "enabled": True,       
    },
        {
        "id": "poweroff",
        "icon": draw_icon_poweroff,
        "run": "EXIT",
        "enabled": True,
    },
]
