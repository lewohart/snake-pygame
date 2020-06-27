import logging
import pygame
import random

logger = logging.getLogger(__name__)

from color import Color


class Apple(object):
    def __init__(self, board):
        self.board = board
        self.x = 0
        self.y = 0
        self.freshen()

    def freshen(self):
        self.x = round(random.randrange(self.board.columns))
        self.y = round(random.randrange(self.board.rows))

        logger.debug(f"Freshen a new apple at ({self.x}, {self.y})")

    def draw(self):
        pygame.draw.circle(
            self.board.screen,
            Color.red,
            self.board.get_point_at(self.x, self.y),
            self.board.cel_width * 0.6,
        )
