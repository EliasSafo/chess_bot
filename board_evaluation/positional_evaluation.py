import chess
from board_evaluation.material_evaluation import MaterialEvaluation
from utils.piece_square_tables import PIECE_SQUARE_TABLES


class PositionalEvaluation:


    @property
    def config_id(self) -> str:
        return "positional"

    def evaluate_board(self, board: chess.Board) -> float:
        material_evaluator = MaterialEvaluation()
        material_evaluation = material_evaluator.evaluate_board(board)
        positional_evaluation = self.positional_evaluate_board(board)
        final_score = material_evaluation + positional_evaluation
        return final_score

    def positional_evaluate_board(self,board:chess.Board) -> float:
        score = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is None:
                continue
            table = PIECE_SQUARE_TABLES[piece.piece_type]
            if piece.color == chess.WHITE:
                value = table[square]
                score += value

            else:
                value = table[chess.square_mirror(square)]
                score -= value


        return score