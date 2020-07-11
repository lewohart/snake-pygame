import logging
from enum import Enum

import pygame

from board import Board
from color import Color
from apple import Apple

logger = logging.getLogger(__name__)


class Snake(object):
    head_size = 10

    def __init__(self, board: Board):
        self.grow = False
        self.reachs_the_border = False
        self.bit_herself = False
        self.looking_direction = pygame.K_UP
        self.new_direction = None
        self.bend_direction = None
        self.board = board

        center = (board.columns // 2, board.rows // 2)

        self.body = [
            (center[0], center[1] - i, self.looking_direction, None) for i in range(10)
        ]
        self.draw = self.draw_core if board.cfg.core_mode else self.draw_sprite

        logger.debug(f"Initial snake {self.body}")

    def head_x(self) -> (int, int):
        return self.body[-1][0]

    def head_y(self) -> (int, int):
        return self.body[-1][1]

    def move(self, pos: (int, int)):
        if not self.grow:
            del self.body[0]
        else:
            self.grow = False

        self.body.append((pos[0], pos[1], self.looking_direction, None))

        if self.bend_direction is not None:
            neck = self.body[-1]
            self.body[-1] = (neck[0], neck[1], neck[2], self.bend_direction)

            self.looking_direction = self.new_direction
            self.bend_direction = None

    def move_pos(self, pos: (int, int)):
        if self.reachs_the_border:
            logger.debug(f"The snake reachs the box border at {pos}")
            return

        self.bit_herself = self.collides(pos)

        if self.bit_herself:
            logger.debug(f"The snake bit itself at {pos}")
            return

        self.move(pos)

    def move_x(self, dx: int):
        x = self.head_x() + dx
        self.reachs_the_border = not self.board.contains_x(x)
        self.move_pos((x, self.head_y()))

    def move_y(self, dy: int):
        y = self.head_y() + dy
        self.reachs_the_border = not self.board.contains_y(y)
        self.move_pos((self.head_x(), y))

    @staticmethod
    def _direction_name(direction) -> str:
        if pygame.K_LEFT:
            return "LEFT"
        elif pygame.K_RIGHT:
            return "RIGHT"
        elif pygame.K_UP:
            return "UP"
        elif pygame.K_DOWN:
            return "DOWN"

        logger.critical("Invalid direction")
        return "Unknown"

    def handle_direction(self, direction, forbidden, right):
        if direction != forbidden:
            if direction == right:
                self.bend_direction = self.board.tile.snake_bend_right
            else:
                self.bend_direction = self.board.tile.snake_bend_left

            self.new_direction = direction

            logger.debug(
                f"The snake turns at ({self.head_x()}, {self.head_y()}) to the %s",
                Snake._direction_name(direction),
            )

    def turn(self, direction):
        if self.looking_direction == direction or direction not in [
            pygame.K_LEFT,
            pygame.K_RIGHT,
            pygame.K_UP,
            pygame.K_DOWN,
        ]:
            return

        if self.looking_direction == pygame.K_LEFT:
            self.handle_direction(direction, pygame.K_RIGHT, pygame.K_UP)
        elif self.looking_direction == pygame.K_RIGHT:
            self.handle_direction(direction, pygame.K_LEFT, pygame.K_DOWN)
        elif self.looking_direction == pygame.K_UP:
            self.handle_direction(direction, pygame.K_DOWN, pygame.K_RIGHT)
        elif self.looking_direction == pygame.K_DOWN:
            self.handle_direction(direction, pygame.K_UP, pygame.K_LEFT)

    def step(self):
        if self.looking_direction == pygame.K_LEFT:
            self.move_x(-1)
        elif self.looking_direction == pygame.K_RIGHT:
            self.move_x(1)
        elif self.looking_direction == pygame.K_UP:
            self.move_y(-1)
        elif self.looking_direction == pygame.K_DOWN:
            self.move_y(1)
        else:
            logger.critical("Invalid direction")

    def eat_the(self, apple: Apple):
        logger.debug(f"The snake ate the apple at ({apple.x}, {apple.y})")
        self.grow = True

    def reachs_the(self, apple: Apple):
        logger.debug(
            f"The snake is trying to eat apple at ({self.head_x()}, {self.head_y()})"
        )
        return self.head_x() == apple.x and self.head_y() == apple.y

    def collides(self, pos: (int, int)):
        for b in self.body:
            if b[0] == pos[0] and b[1] == pos[1]:
                return True

        return False

    def get_body_tile(self, direction, bend_direction):
        if bend_direction == self.board.tile.snake_bend_right:
            return self.board.tile.get_bend_right(direction)
        elif bend_direction == self.board.tile.snake_bend_left:
            return self.board.tile.get_bend_left(direction)
        else:
            return self.board.tile.get_body(direction)

    def draw_core(self):
        for b in self.body:
            pygame.draw.rect(
                self.board.screen, Color.BLACK, self.board.get_rect_at(b[0], b[1])
            )

    def draw_sprite(self):
        x, y, direction, bend = self.body[-1]
        head = self.board.tile.get_head(direction)
        self.board.screen.blit(head, self.board.get_rect_at(x, y))

        for x, y, direction, bend in self.body[1:-1]:
            tile = self.get_body_tile(direction, bend)
            self.board.screen.blit(tile, self.board.get_rect_at(x, y))

        x, y, _, _ = self.body[0]
        direction = self.body[1][2]
        tile = self.board.tile.get_tail(direction)
        self.board.screen.blit(tile, self.board.get_rect_at(x, y))
