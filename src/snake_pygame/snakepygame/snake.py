import logging
import pygame

from color import Color
from board import Board
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

        center = (int(board.rows / 2), int(board.columns / 2))
        self.body = [(center[0], center[1] - i) for i in range(4)]
        logger.debug(f"Initial snake {self.body}")

    def head_x(self) -> (int, int):
        return self.body[-1][0]

    def head_y(self) -> (int, int):
        return self.body[-1][1]

    def move_pos(self, pos: (int, int)):
        if self.reachs_the_border:
            logger.debug(f"The snake reachs the box border at {pos}")
            return

        self.bit_herself = self.collides(pos)

        if self.bit_herself:
            logger.debug(f"The snake bit itself at {pos}")
            return

        self.body.append(pos)

        if not self.grow:
            del self.body[0]
        else:
            self.grow = False

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

        return "UNKNOWN"

    def turn(self, direction):
        if direction not in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            return

        if (
            (self.looking_to == pygame.K_LEFT and direction == pygame.K_RIGHT)
            or (self.looking_to == pygame.K_RIGHT and direction == pygame.K_LEFT)
            or (self.looking_to == pygame.K_UP and direction == pygame.K_DOWN)
            or (self.looking_to == pygame.K_DOWN and direction == pygame.K_UP)
        ):
            return

        logger.debug(
            f"The snake turns at ({self.head_x()}, {self.head_y()}) to the %s",
            Snake._direction_name(direction),
        )
        self.looking_to = direction

    def move(self):
        if self.looking_to == pygame.K_LEFT:
            self.move_x(-1)
        elif self.looking_to == pygame.K_RIGHT:
            self.move_x(1)
        elif self.looking_to == pygame.K_UP:
            self.move_y(-1)
        elif self.looking_to == pygame.K_DOWN:
            self.move_y(1)

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

    def draw(self):
        for b in self.body:
            pygame.draw.rect(
                self.board.screen, Color.black, self.board.get_rect_at(b[0], b[1])
            )
