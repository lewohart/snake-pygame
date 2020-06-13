import logging
import pygame
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

display_size = (800, 600)


class Color(object):
    black = (0, 0, 0)
    blue = (0, 0, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)


class Snake(object):
    head_size = 10

    def __init__(self, screen):
        self.collided = False
        self.screen_size = screen.get_size()
        self.size = Snake.head_size

        self.screen = screen
        self.body = [(self.screen_size[0] / 2, self.screen_size[1] / 2)]

    def move_x(self, dx):
        x = self.body[-1][0] + dx
        self.collided = not (0 <= x and x <= self.screen_size[0] - self.size)

        if not self.collided:
            self.body.append((x, self.body[-1][1]))

    def move_y(self, dy):
        y = self.body[-1][1] + dy
        self.collided = not (0 <= y and y <= self.screen_size[1] - self.size)

        if not self.collided:
            self.body.append((self.body[-1][0], y))

    def move(self, key):
        if key == pygame.K_LEFT:
            self.move_x(-10)
        elif key == pygame.K_RIGHT:
            self.move_x(10)
        elif key == pygame.K_UP:
            self.move_y(-10)
        elif key == pygame.K_DOWN:
            self.move_y(10)

        self.draw()

    def draw(self):
        for b in self.body:
            pygame.draw.rect(self.screen, Color.black,
                             [b[0], b[1], self.size, self.size])


class Food(object):
    size = 10

    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen, Color.green,
                         [400, 300, Food.size, Food.size])


if __name__ == "__main__":
    game_quit = False
    last_key = -1

    pygame.init()
    pygame.display.set_caption("Snake - by lewohart")

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    snake = Snake(screen)
    food = Food(screen)

    while not (game_quit or snake.collided):
        for event in pygame.event.get():
            logger.debug(event)

            if event.type == pygame.QUIT:
                game_quit = True
                break

            if event.type == pygame.KEYDOWN:
                last_key = event.key

        screen.fill(Color.white)

        snake.move(last_key)
        food.draw()

        pygame.display.update()
        clock.tick(30)

    logger.debug("Finish event loop")
    font_style = pygame.font.SysFont(None, 50)
    text = font_style.render("Game over", True, Color.red)
    screen.blit(text, [display_size[0] / 2, display_size[1] / 2])

    pygame.display.update()
    time.sleep(2)
    pygame.quit()
    quit(0)
