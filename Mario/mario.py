import pygame
import random

from Settings.output import draw_matrix_representation, draw_matrix, draw_score, draw_shaded_block
from Settings.colors import *
from Settings.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE
from Settings import inputs


def mario_game(screen, matrix, offset_canvas, started_on_pi, input_handler: inputs.InputHandler):
    print("mario läuft!")