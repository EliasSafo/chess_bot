import chess


class MaterialEvaluation:
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 0,
    }

    @property
    def config_id(self) -> str:
        return "material"

    def evaluate_board(self, board: chess.Board) -> float:
        checkmate_score = self.checkmate_score(board)

        if checkmate_score != 0:
            return checkmate_score

        score = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)

            if piece is None:
                continue

            value = self.PIECE_VALUES[piece.piece_type]

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        return score

    def checkmate_score(self, board: chess.Board) -> float:
        if not board.is_checkmate():
            return 0

        # The player whose turn it is has been checkmated.
        if board.turn == chess.WHITE:
            return -999999

        return 999999