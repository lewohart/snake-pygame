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
        self.looking_to = pygame.K_UP
        self.board = board

        center = (board.rows // 2, board.columns // 2)

        self.board.tile.set_direction(self.looking_to)
        self.body = [(center[0], center[1] - i, self.board.tile.get_body()) for i in range(4)]
        self.draw = self.draw_core if board.cfg.core_mode else self.draw_sprite

        self.bend_to = None
        self.bend_right = board.tile.snake_bend_right
        self.bend_left = board.tile.snake_bend_left

        logger.debug(f"Initial snake {self.body}")


    def head_x(self) -> (int, int):
        return self.body[-1][0]

    def head_y(self) -> (int, int):
        return self.body[-1][1]

    def move(self,pos: (int, int)):
        x, y = self.body[-1][0], self.body[-1][1]

        if self.bend_to == self.bend_right:
            neck = (x, y, self.board.tile.get_bend_right())
        elif self.bend_to == self.bend_left:
            neck = (x, y, self.board.tile.get_bend_left())
        else:
            neck = (x, y, self.board.tile.get_body())

        self.body[-1] = neck
        self.bend_to = None

        if not self.grow:
            del self.body[0]
            x, y = self.body[0][0], self.body[0][1]
            self.body[0] = (x, y, self.board.tile.get_tail())
        else:
            self.grow = False

        self.board.tile.set_direction(self.looking_to)
        self.body.append((pos[0], pos[1], self.board.tile.get_head()))

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

    def turn(self, direction):
        if direction not in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            return

        if self.looking_to == direction:
            return

        if self.looking_to == pygame.K_LEFT:
            if direction == pygame.K_RIGHT:
                return

            self.bend_to = self.bend_right if direction == pygame.K_UP else self.bend_left

        elif self.looking_to == pygame.K_RIGHT:
            if direction == pygame.K_LEFT:
                return

            self.bend_to = self.bend_right if direction == pygame.K_DOWN else self.bend_left

        elif self.looking_to == pygame.K_UP:
            if direction == pygame.K_DOWN:
                return

            self.bend_to = self.bend_right if direction == pygame.K_RIGHT else self.bend_left

        elif self.looking_to == pygame.K_DOWN:
            if direction == pygame.K_UP:
                return

            self.bend_to = self.bend_right if direction == pygame.K_LEFT else self.bend_left

        else:
            logger.warning(f"The snake tried to turn to an invalid directions ({direction})")
            return

        logger.debug(
            f"The snake turns at ({self.head_x()}, {self.head_y()}) to the %s",
            Snake._direction_name(direction),
        )

        self.looking_to = direction

    def step(self):
        if self.looking_to == pygame.K_LEFT:
            self.move_x(-1)
        elif self.looking_to == pygame.K_RIGHT:
            self.move_x(1)
        elif self.looking_to == pygame.K_UP:
            self.move_y(-1)
        elif self.looking_to == pygame.K_DOWN:
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
        return pos in self.body

    def draw_core(self):
        for b in self.body:
            pygame.draw.rect(
                self.board.screen, Color.BLACK, self.board.get_rect_at(b[0], b[1])
            )

    def draw_sprite(self):
        for b in self.body:
            x, y, tile = b[0], b[1], b[2]
            self.board.screen.blit(tile, self.board.get_rect_at(x, y))
