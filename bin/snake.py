import logging
import pygame

import time


class Snake(object):
    head_size = 10

    def __init__(self, board: Board):
        self.grow = False
        self.reachs_the_border = False
        self.bit_herself = False
        self.board = board

        center = (board.rows / 2, board.columns / 2)
        self.body = [(center[0], center[1] + i) for i in range(0, 4)]

    def head_x(self) -> (int, int):
        return self.body[-1][0]

    def head_y(self) -> (int, int):
        return self.body[-1][1]

    def move_pos(self, pos: (int, int)):
        self.bit_herself = self.collides(pos)
        self.body.append(pos)

        if not self.grow:
            del self.body[0]
        else:
            self.grow = False

    def move_x(self, dx: int):
        x = self.head_x() + dx
        self.reachs_the_border = not (0 <= x and x <= self.board.rows)

        if not self.reachs_the_border:
            self.move_pos((x, self.head_y()))

    def move_y(self, dy: int):
        y = self.head_y() + dy
        self.reachs_the_border = not (0 <= y and y <= self.board.columns)

        if not self.reachs_the_border:
            self.move_pos((self.head_x(), y))

    def move(self, key):
        if key == pygame.K_LEFT:
            self.move_x(-1)
        elif key == pygame.K_RIGHT:
            self.move_x(1)
        elif key == pygame.K_UP:
            self.move_y(-1)
        elif key == pygame.K_DOWN:
            self.move_y(1)

    def eat_the(self, apple: Apple):
        self.grow = True

    def reachs_the(self, apple: Apple):
        logger.debug(
            f"Snakes at ({self.head_x()}, {self.head_y()}) trying to eat apple at ({apple.x}, {apple.y})"
        )
        return self.head_x() == apple.x and self.head_y() == apple.y

    def collides(self, pos: (int, int)):
        return pos in self.body

    def draw(self):
        for b in self.body:
            pygame.draw.rect(
                self.board.screen, Color.black, self.board.get_rect_at(b[0], b[1])
            )
