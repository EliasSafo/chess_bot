import random

import chess

from bots.base_bot import BaseBot


class RandomBot(BaseBot):

    def choose_move(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)

        if not legal_moves:
            raise ValueError("No legal moves available")

        return random.choice(legal_moves)