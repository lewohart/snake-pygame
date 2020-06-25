#!/usr/bin/env python

import argparse
import pygame
import logging

logger = logging.getLogger("snake-pygame")


def main():
    cfg = _parse_args()
    common.setup_logging(cfg.verbose)

    game_quit = False
    last_key = pygame.K_DOWN

    pygame.init()
    pygame.display.set_caption("Snake - by lewohart")
    clock = pygame.time.Clock()

    display = pygame.Rect(0, 0, 800, 600)
    box = display.inflate(-200, -100)
    rows = display.width / 10
    columns = display.height / 10

    screen = pygame.display.set_mode(display.size)
    board = Board(screen, display, box, rows, columns)
    snake = Snake(board)
    apple = Apple(board)

    def on_quit(e):
        global game_quit
        game_quit = True

    def on_key_down(e):
        global last_key
        if e.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
            last_key = e.key
        else:
            last_key = -1

    while not (game_quit or snake.reachs_the_border or snake.bit_herself):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on_quit(event)
            elif event.type == pygame.KEYDOWN:
                on_key_down(event)

        screen.fill(Color.white)

        if last_key != -1:
            snake.move(last_key)

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
    screen.blit(text, [display_size[0] / 2, display_size[1] / 2])

    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit(0)


def _parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Increase verbosity"
    )

    cfg = parser.parse_args()

    return cfg
