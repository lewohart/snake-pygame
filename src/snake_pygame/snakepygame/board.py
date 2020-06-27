import pygame

from color import Color


class Board(object):
    def __init__(
        self,
        screen,
        display: pygame.Rect,
        box: pygame.Rect,
        rows: int,
        columns: int,
        draw_grid: bool = False,
    ):
        self.screen = screen
        self.display = display
        self.box = box
        self.rows = int(rows)
        self.columns = int(columns)

        self.cel_height = box.height / (rows + 1)
        self.cel_width = box.width / (columns + 1)
        self.on_draw_grid = self.on_draw_grid_active if draw_grid else lambda: None

    def get_rect_at(self, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(
            (self.box.left + ((x + 1) * self.cel_width)) - (self.cel_width / 2),
            (self.box.top + ((y + 1) * self.cel_height)) - (self.cel_height / 2),
            self.cel_width,
            self.cel_height,
        )

    def get_point_at(self, x: int, y: int) -> (int, int):
        return (
            self.box.left + ((x + 1) * self.cel_width),
            self.box.top + ((y + 1) * self.cel_height),
        )

    def on_draw_grid_active(self):
        max_y = self.rows
        max_x = self.columns

        for x in range(max_x):
            pygame.draw.line(
                self.screen,
                Color.white_smoke,
                self.get_point_at(x, 0),
                self.get_point_at(x, max_y - 1),
                1,
            )

        for y in range(max_y):
            pygame.draw.line(
                self.screen,
                Color.white_smoke,
                self.get_point_at(0, y),
                self.get_point_at(max_x - 1, y),
                1,
            )

    def draw(self):
        self.screen.fill(Color.white)
        pygame.draw.rect(self.screen, Color.black, self.box, 1)
        self.on_draw_grid()

    def contains_x(self, x: int):
        return 0 <= x and x < self.columns

    def contains_y(self, y: int):
        return 0 <= y and y < self.rows
