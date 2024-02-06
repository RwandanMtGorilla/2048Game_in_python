## game.py
from ui import UI
from logic import Logic
from constants import Constants

class Game:
    """
    Game class manages the game state, including the score, high score, and the game board.
    It interacts with the UI class to display the game and the Logic class to handle the game logic.
    """
    
    def __init__(self):
        """
        Initializes the game with a score of 0, a high score of 0, and an empty game board.
        """
        self._score = 0
        self._high_score = 0
        self._board = [[0 for _ in range(Constants.BOARD_SIZE)] for _ in range(Constants.BOARD_SIZE)]
        self._ui = UI()
        self._logic = Logic()
        self._previous_states = []

    def start_game(self):
        """
        Starts the game by placing the initial tiles and entering the game loop.
        """
        for _ in range(Constants.INITIAL_TILES):
            self._board = self._logic.generate_new_tile(self._board)
        self._ui.draw_board(self._board)
        self._ui.display_score(self._score)
        self._ui.display_high_score(self._high_score)
        self.game_loop()

    def reset_game(self):
        """
        Resets the game to the initial state with a new board, score, and high score.
        """
        self._score = 0
        self._board = [[0 for _ in range(Constants.BOARD_SIZE)] for _ in range(Constants.BOARD_SIZE)]
        for _ in range(Constants.INITIAL_TILES):
            self._board = self._logic.generate_new_tile(self._board)
        self._ui.draw_board(self._board)
        self._ui.display_score(self._score)
        self._ui.display_high_score(self._high_score)

    def make_move(self, direction: str) -> bool:
        """
        Makes a move in the given direction, updates the game state, and returns whether the move was valid.

        :param direction: The direction to move the tiles ('up', 'down', 'left', 'right').
        :return: True if the move was valid, False otherwise.
        """
        new_board, score_increment = self._logic.merge_tiles(self._board, direction)
        if new_board != self._board:
            self._previous_states.append((self._board, self._score))
            self._board = new_board
            self._score += score_increment
            if self._score > self._high_score:
                self._high_score = self._score
            self._board = self._logic.generate_new_tile(self._board)
            self._ui.draw_board(self._board)
            self._ui.display_score(self._score)
            self._ui.display_high_score(self._high_score)
            return True
        return False

    def undo_move(self) -> bool:
        """
        Undoes the last move, if possible, and returns whether the undo was successful.

        :return: True if the undo was successful, False otherwise.
        """
        if self._previous_states:
            self._board, self._score = self._previous_states.pop()
            self._ui.draw_board(self._board)
            self._ui.display_score(self._score)
            self._ui.display_high_score(self._high_score)
            return True
        return False

    def game_loop(self):
        """
        The main game loop that waits for user input and processes the game logic.
        """
        running = True
        while running:
            direction = self._ui.get_user_input()
            if direction == 'quit':
                running = False
            elif direction in ('up', 'down', 'left', 'right'):
                valid_move = self.make_move(direction)
                if not valid_move:
                    self._ui.draw_board(self._board)  # Redraw unchanged board
