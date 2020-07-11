import random
from argparse import Namespace

import pygame

from color import Color
from tile import Tile


class Board(object):
    def __init__(
        self,
        screen,
        display: pygame.Rect,
        box: pygame.Rect,
        columns: int,
        rows: int,
        cfg: Namespace,
    ):
        self.background_color = Color.WHITE
        self.screen = screen
        self.display = display
        self.box = box
        self.columns = int(columns)
        self.rows = int(rows)
        self.cfg = cfg

        self.cell_width = round(box.width / (columns + 1))
        self.cell_height = round(box.height / (rows + 1))

        self.tile = (
            Tile(self.cell_width, self.cell_height) if not cfg.core_mode else None
        )
        self.on_draw_grid = self.on_draw_grid_active if cfg.draw_grid else lambda: None

    def get_rect_at(self, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            (self.box.left + ((x + 1) * self.cell_width)) - (self.cell_width / 2),
            (self.box.top + ((y + 1) * self.cell_height)) - (self.cell_height / 2),
            self.cell_width,
            self.cell_height,
        )

    def get_point_at(self, x: int, y: int) -> (int, int):
        return (
            self.box.left + ((x + 1) * self.cell_width),
            self.box.top + ((y + 1) * self.cell_height),
        )

    def on_draw_grid_active(self):
        max_y = self.rows
        max_x = self.columns

        for x in range(max_x):
            pygame.draw.line(
                self.screen,
                Color.WHITE_SMOKE,
                self.get_point_at(x, 0),
                self.get_point_at(x, max_y - 1),
                1,
            )

        for y in range(max_y):
            pygame.draw.line(
                self.screen,
                Color.WHITE_SMOKE,
                self.get_point_at(0, y),
                self.get_point_at(max_x - 1, y),
                1,
            )

    def draw(self):
        self.screen.fill(self.background_color)
        pygame.draw.rect(self.screen, Color.BLACK, self.box, 1)
        self.on_draw_grid()

    def contains_x(self, x: int):
        return 0 <= x and x < self.columns

    def contains_y(self, y: int):
        return 0 <= y and y < self.rows

    def get_available_cell(self, snake) -> (int, int):
        while True:
            available_cell = (
                round(random.randrange(self.columns)),
                round(random.randrange(self.rows)),
            )

            if not snake.collides(available_cell):
                return available_cell
