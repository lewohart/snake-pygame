import logging

import pygame

logger = logging.getLogger(__name__)

from color import Color


class Apple(object):
    def __init__(self, board):
        self.board = board
        self.x = 0
        self.y = 0
        self.draw = self.draw_core if board.cfg.core_mode else self.draw_sprite

    def yield_away_from_the(self, snake):
        available_cell = self.board.get_available_cell(snake)
        self.x = available_cell[0]
        self.y = available_cell[1]
        logger.debug(f"Freshen a new apple at ({self.x}, {self.y})")

    def draw_core(self):
        pygame.draw.circle(
            self.board.screen,
            Color.RED,
            self.board.get_point_at(self.x, self.y),
            self.board.cell_width,
        )

    def draw_sprite(self):
        self.board.screen.blit(self.board.tile.get_apple(), self.board.get_rect_at(self.x, self.y))
