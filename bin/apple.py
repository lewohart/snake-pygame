import logging
import random

logger = logging.getLogger(__name__)


class Apple(object):
    def __init__(self, board):
        self.board = board
        self.freshen()

    def freshen(self):
        self.x = round(random.randrange(0, self.board.rows))
        self.y = round(random.randrange(0, self.board.columns))

        logger.debug(f"Freshen a new apple at ({self.x}, {self.y})")

    def draw(self):
        pygame.draw.circle(
            self.board.screen,
            Color.red,
            self.board.get_point_at(self.x, self.y),
            self.board.cel_width * 0.6,
        )
