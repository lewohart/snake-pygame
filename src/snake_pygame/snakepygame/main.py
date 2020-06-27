#!/usr/bin/env python

import argparse
import logging
import sys

import pygame
import time

from snakepygame import common

from color import Color
from board import Board
from apple import Apple
from snake import Snake

logger = logging.getLogger("snake-pygame")


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase verbosity"
    )
    parser.add_argument(
        "-g", "--draw-grid", action="store_true", help="Draw background grid"
    )
    cfg = parser.parse_args()

    return cfg


def main():
    cfg = _parse_args()
    common.setup_logging(cfg.verbose)
    game_quit = False

    pygame.init()
    pygame.display.set_caption("Snake - by lewohart")
    clock = pygame.time.Clock()

    display = pygame.Rect(0, 0, 800, 600)
    box = display.inflate(-200, -100)
    columns = int(box.width / 10)
    rows = int(box.height / 10)

    screen = pygame.display.set_mode(display.size)
    board = Board(screen, display, box, rows, columns, cfg.draw_grid)
    snake = Snake(board)
    apple = Apple(board)

    while not (game_quit):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            elif event.type == pygame.KEYDOWN:
                snake.turn(event.key)

        snake.move()

        if snake.reachs_the_border or snake.bit_herself:
            break

        if snake.reachs_the(apple):
            snake.eat_the(apple)
            apple.freshen()

        board.draw()
        apple.draw()
        snake.draw()

        pygame.display.flip()

        clock.tick(20)

    font_style = pygame.font.SysFont(None, 50)
    text = font_style.render("Game over", True, Color.red)
    screen.blit(text, screen)

    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    quit(0)


if __name__ == "__main__":
    sys.exit(main())
