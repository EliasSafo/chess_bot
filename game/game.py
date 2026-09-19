import chess


class Game:

    def __init__(self):
        self.board = chess.Board()

    def make_move(self, move: chess.Move) -> bool:
        if move not in self.board.legal_moves:
            return False

        self.board.push(move)

        return True

    def reset(self):
        self.board.reset()

    def is_over(self) -> bool:
        return self.board.is_game_over()