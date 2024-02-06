## ui.py
import pygame
from constants import Constants

class UI:
    """
    UI class is responsible for rendering the game interface, displaying the game board,
    score, high score, and handling user input.
    """

    def __init__(self):
        """
        Initializes the UI components and sets up the display.
        """
        pygame.init()
        self.tile_size = 100
        self.tile_margin = 15
        self.screen_width = Constants.BOARD_SIZE * (self.tile_size + self.tile_margin) + self.tile_margin
        self.screen_height = self.screen_width + 100  # Extra space for score display
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('2048 Game')
        self.font = pygame.font.SysFont(None, 48)
        self.colors = {
            0: (205, 193, 180),
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46),
        }

    def draw_tile(self, value, x, y):
        """
        Draws an individual tile on the game board.

        :param value: The value of the tile to draw.
        :param x: The x-coordinate of the tile.
        :param y: The y-coordinate of the tile.
        """
        tile_color = self.colors.get(value, (0, 0, 0))
        tile_position = (
            y * (self.tile_size + self.tile_margin) + self.tile_margin,
            x * (self.tile_size + self.tile_margin) + self.tile_margin
        )
        pygame.draw.rect(self.screen, tile_color,
                         (tile_position[0], tile_position[1], self.tile_size, self.tile_size))
        if value:
            text_surface = self.font.render(str(value), True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(
                tile_position[0] + self.tile_size / 2,
                tile_position[1] + self.tile_size / 2
            ))
            self.screen.blit(text_surface, text_rect)

    def draw_board(self, board: list):
        """
        Draws the game board on the screen.

        :param board: The current state of the game board.
        """
        self.screen.fill(self.colors[0])
        for x in range(Constants.BOARD_SIZE):
            for y in range(Constants.BOARD_SIZE):
                self.draw_tile(board[x][y], x, y)
        pygame.display.update()

    def display_score(self, score: int):
        """
        Displays the current score on the screen.

        :param score: The current score.
        """
        self.display_text(f'Score: {score}', self.screen_width / 2, self.screen_height - 50)

    def display_high_score(self, high_score: int):
        """
        Displays the high score on the screen.

        :param high_score: The high score.
        """
        self.display_text(f'High Score: {high_score}', self.screen_width / 2, self.screen_height - 20)

    def display_text(self, text: str, x: float, y: float):
        """
        Helper method to display text on the screen.

        :param text: The text to display.
        :param x: The x-coordinate of the text's center.
        :param y: The y-coordinate of the text's center.
        """
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)
        pygame.display.update()

    def get_user_input(self) -> str:
        """
        Waits for and returns the user input as a string representing the direction.

        :return: A string representing the direction of the move ('up', 'down', 'left', 'right').
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return 'up'
                elif event.key == pygame.K_DOWN:
                    return 'down'
                elif event.key == pygame.K_LEFT:
                    return 'left'
                elif event.key == pygame.K_RIGHT:
                    return 'right'
        return ''
