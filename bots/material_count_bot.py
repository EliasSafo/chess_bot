import random

import chess

from bots.base_bot import BaseBot
from evaluation.material import MaterialEvaluation

class MaterialCountBot(BaseBot):

    def __init__(self):
        self.evaluator = MaterialEvaluation()
        self.depth = 0

    def choose_move(self, board: chess.Board) -> chess.Move:
        legal_moves = list(board.legal_moves)

        if not legal_moves:
            raise ValueError("No legal moves available")
        move_evaluations = []
        for move in legal_moves:
            board.push(move)
            evaluation =self.evaluator.evaluate_board(board)
            board.pop()
            move_evaluations.append((move, evaluation))

        if board.turn == chess.WHITE:
            best_move = max(evaluation for move, evaluation in move_evaluations)
        else:
            best_move= min(evaluation for move, evaluation in move_evaluations)

        best_moves = [move for move, evaluation in move_evaluations if evaluation == best_move]
        return random.choice(best_moves)