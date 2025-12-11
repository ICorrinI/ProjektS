import pygame
import Settings.colors as fc
import Settings.settings as s


def draw_icon_x(screen, x_offset, y_offset):
    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, s.SCREEN_HALF))
    pygame.draw.line(
        screen, fc.GRAY,
        (x_offset + 20, y_offset + 20),
        (x_offset + s.SCREEN_HALF - 20, y_offset + s.SCREEN_HALF - 20),
        s.PIXEL_WIDTH
    )
    pygame.draw.line(
        screen, fc.GRAY,
        (x_offset + s.SCREEN_HALF - 20, y_offset + 20),
        (x_offset + 20, y_offset + s.SCREEN_HALF - 20),
        s.PIXEL_WIDTH
    )


def draw_icon_snake(screen, x_offset, y_offset):
    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, s.SCREEN_HALF))

    pygame.draw.rect(screen, fc.GREEN, (x_offset + 0,   y_offset + 200, 140, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 60,  y_offset + 160, 80,  s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 60,  y_offset + 120, 160, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 200, y_offset + 140, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 60,  y_offset + 140, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.GREEN, (x_offset + 120, y_offset + 180, s.PIXEL_WIDTH, s.PIXEL_WIDTH))
    pygame.draw.rect(screen, fc.RED, (x_offset + 200, y_offset + 200, s.PIXEL_WIDTH, s.PIXEL_WIDTH))


def draw_icon_poweroff(screen, x_offset, y_offset):
    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, s.SCREEN_HALF))

    pygame.draw.circle(
        screen,
        fc.RED,
        (x_offset + 470 - s.SCREEN_HALF, y_offset + 471 + s.DOWNWARD_PIXEL_PULL_OFFSET - s.SCREEN_HALF),
        129,
        s.PIXEL_WIDTH
    )

    pygame.draw.rect(screen, fc.BLACK, (x_offset, y_offset, s.SCREEN_HALF, 60))
    pygame.draw.rect(screen, fc.RED, (x_offset + 140, y_offset + 40, 40, 120))
