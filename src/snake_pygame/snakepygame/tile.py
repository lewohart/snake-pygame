import pygame


class Tile(object):
    snake_head = 0
    snake_body = 1
    snake_bend_left = 2
    snake_bend_right = 3
    snake_tail = 4
    apple = 5

    def __init__(self, cell_width, cell_height):
        self.filename = "../data/snake.png"
        self.columns = 5
        self.rows = 4
        self.image = pygame.transform.scale(
            pygame.image.load(self.filename),
            (int(cell_width * self.columns), int(cell_height * self.rows)),
        ).convert()

        self.tile_table = self.__build_index()

        """                 Head    Body    Left    Right   Tail   """
        self.snake_left = ((3, 1), (1, 0), (0, 0), (0, 1), (3, 3))
        self.snake_right = ((4, 0), (1, 0), (2, 2), (2, 0), (4, 2))
        self.snake_up = ((3, 0), (2, 1), (2, 0), (0, 0), (3, 2))
        self.snake_down = ((4, 1), (2, 1), (0, 1), (2, 2), (4, 3))

        self.apple_pos = (0, 3)

    def __build_index(self):
        image_width, image_height = self.image.get_size()
        tile_width = image_width // self.columns
        tile_height = image_height // self.rows

        tile_table = []

        for tile_x in range(self.columns):
            line = []

            for tile_y in range(self.rows):
                rect = (
                    tile_x * tile_width,
                    tile_y * tile_height,
                    tile_width,
                    tile_height,
                )
                row = self.image.subsurface(rect)
                line.append(row)

            tile_table.append(line)

        return tile_table

    def get_direction(self, direction):
        if direction == pygame.K_LEFT:
            return self.snake_left
        elif direction == pygame.K_RIGHT:
            return self.snake_right
        elif direction == pygame.K_UP:
            return self.snake_up
        elif direction == pygame.K_DOWN:
            return self.snake_down
        else:
            raise RuntimeError("Invalid direction")

    def get_tile_for(self, part, direction):
        snake_parts = self.get_direction(direction)
        body_part = snake_parts[part]
        col, row = body_part[0], body_part[1]
        return self.tile_table[col][row]

    def get_head(self, direction) -> pygame.Surface:
        return self.get_tile_for(Tile.snake_head, direction)

    def get_body(self, direction) -> pygame.Surface:
        return self.get_tile_for(Tile.snake_body, direction)

    def get_bend_left(self, direction) -> pygame.Surface:
        return self.get_tile_for(Tile.snake_bend_left, direction)

    def get_bend_right(self, direction) -> pygame.Surface:
        return self.get_tile_for(Tile.snake_bend_right, direction)

    def get_tail(self, direction) -> pygame.Surface:
        return self.get_tile_for(Tile.snake_tail, direction)

    def get_apple(self) -> pygame.Surface:
        col = self.apple_pos[0]
        row = self.apple_pos[1]
        return self.tile_table[col][row]
