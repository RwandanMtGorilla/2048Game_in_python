## logic.py
import random
from constants import Constants

class Logic:
    """
    Logic class contains the core game logic for the 2048 game.
    It is responsible for generating new tiles and merging tiles on the board.
    """

    @staticmethod
    def generate_new_tile(board: list) -> list:
        """
        Generates a new tile on the board in a random empty position.
        The new tile will be either 2 or 4, with a 90% chance of being a 2.

        :param board: The current state of the game board.
        :return: The updated board with a new tile.
        """
        empty_positions = [(x, y) for x in range(Constants.BOARD_SIZE) for y in range(Constants.BOARD_SIZE) if board[x][y] == 0]
        if not empty_positions:
            return board

        x, y = random.choice(empty_positions)
        board[x][y] = 4 if random.random() > 0.9 else 2
        return board

    @staticmethod
    def merge_tiles(board: list, direction: str) -> tuple:
        """
        Merges the tiles on the board in the given direction.
        This function handles the movement and combination of tiles.

        :param board: The current state of the game board.
        :param direction: The direction to merge the tiles ('up', 'down', 'left', 'right').
        :return: A tuple containing the new board state and the score increment resulting from the merge.
        """
        def move(row):
            """Helper function to move the tiles in a single row or column."""
            new_row = [i for i in row if i != 0]
            new_row += [0] * (Constants.BOARD_SIZE - len(new_row))
            return new_row

        def combine(row):
            """Helper function to combine the tiles in a single row or column."""
            score_increment = 0
            for i in range(len(row) - 1):
                if row[i] != 0 and row[i] == row[i + 1]:
                    row[i] *= 2
                    score_increment += row[i]
                    row[i + 1] = 0
            return score_increment

        score_increment = 0
        rotated = False
        if direction in ('up', 'down'):
            # Rotate the board to simplify merging
            board = [list(x) for x in zip(*board)]
            rotated = True
            if direction == 'down':
                board = [row[::-1] for row in board]

        for i in range(Constants.BOARD_SIZE):
            board[i] = move(board[i])
            score_increment += combine(board[i])
            board[i] = move(board[i])

        if rotated:
            if direction == 'down':
                board = [row[::-1] for row in board]
            # Rotate the board back to its original orientation
            board = [list(x) for x in zip(*board)]

        return board, score_increment
