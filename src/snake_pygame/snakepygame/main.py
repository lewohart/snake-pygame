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
from tile import Tile

logger = logging.getLogger("snake-pygame")


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase verbosity"
    )
    parser.add_argument(
        "-g", "--draw-grid", action="store_true", help="Draw background grid"
    )
    parser.add_argument(
        "-c", "--core-mode", action="store_true", help="Draw using shapes"
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

    display = pygame.Rect(0, 0, 1000, 800)
    box = display.inflate(-200, -100)
    columns = box.width // 20
    rows = box.height // 20

    screen = pygame.display.set_mode(display.size)
    board = Board(screen, display, box, columns, rows, cfg)
    snake = Snake(board)
    apple = Apple(board)

    apple.yield_away_from_the(snake)

    while not (game_quit):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit = True
            elif event.type == pygame.KEYDOWN:
                snake.turn(event.key)

        snake.step()

        if snake.reachs_the_border or snake.bit_herself:
            break

        if snake.reachs_the(apple):
            snake.eat_the(apple)
            apple.yield_away_from_the(snake)

        board.draw()
        apple.draw()
        snake.draw()

        pygame.display.flip()

        clock.tick(5)

    font_style = pygame.font.SysFont(pygame.font.get_default_font(), 50)
    text = font_style.render("Game over", True, Color.RED)
    text_rect = text.get_rect(center=display.center)
    screen.blit(text, text_rect)

    pygame.display.flip()
    time.sleep(4)
    pygame.quit()
    quit(0)


def show_tile():
    common.setup_logging(True)
    pygame.init()
    screen = pygame.display.set_mode((320, 256))
    screen.fill((255, 255, 255))
    tile = Tile(32, 32)
    tile.set_direction(pygame.K_DOWN)

    screen.blit(tile.get_tail(), (0, 0))
    screen.blit(tile.get_body(), (0, 32))
    screen.blit(tile.get_head(), (0, 64))

    screen.blit(tile.get_bend_left(), (32, 0))
    screen.blit(tile.get_bend_right(), (64, 0))


    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
