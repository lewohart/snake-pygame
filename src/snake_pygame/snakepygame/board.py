import pygame


class Board(object):
    def __init__(
        self, screen, display: pygame.Rect, box: pygame.Rect, rows: int, columns: int
    ):
        self.screen = screen
        self.display = display
        self.box = box
        self.rows = int(rows)
        self.columns = int(columns)

        self.cel_width = box.width / (rows + 1)
        self.cel_height = box.height / (columns + 1)

    def get_rect_at(self, row: int, col: int) -> pygame.Rect:
        return pygame.Rect(
            (box.left + ((row + 1) * self.cel_width)) - (self.cel_width / 2),
            (box.top + ((col + 1) * self.cel_height)) - (self.cel_height / 2),
            self.cel_width,
            self.cel_height,
        )

    def get_point_at(self, row: int, col: int) -> (int, int):
        return (
            box.left + ((row + 1) * self.cel_width),
            box.top + ((col + 1) * self.cel_height),
        )

    def draw(self):
        pygame.draw.rect(self.screen, Color.black, box, 1)

        for i in range(self.rows):
            pygame.draw.line(
                self.screen,
                Color.white_smoke,
                self.get_point_at(i, 0),
                self.get_point_at(i, self.columns - 1),
                1,
            )

        for i in range(self.columns):
            pygame.draw.line(
                self.screen,
                Color.white_smoke,
                self.get_point_at(0, i),
                self.get_point_at(self.rows - 1, i),
                1,
            )
