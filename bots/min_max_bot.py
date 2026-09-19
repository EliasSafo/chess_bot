import random

import chess
from bots.base_bot import BaseBot
from evaluation.material import MaterialEvaluation


class MinMaxBot(BaseBot):
    def __init__(self,evaluator,depth:int=2):
        self.depth = depth
        self.evaluator = evaluator
        self.name = "MinMaxBot"


    def choose_move(self, board: chess.Board) -> chess.Move:
            legal_moves = list(board.legal_moves)
            move_evaluations = []
            search_depth = self.depth

            for move in legal_moves:
                board.push(move)
                evaluation = self.min_max(board,search_depth, float("-inf"), float("inf"))
                board.pop()
                move_evaluations.append((move, evaluation))

            if board.turn == chess.WHITE:
                best_move = max(evaluation for move, evaluation in move_evaluations)
            else:
                best_move = min(evaluation for move, evaluation in move_evaluations)

            best_moves = [move for move, evaluation in move_evaluations if evaluation == best_move]

            return random.choice(best_moves)

    def min_max(self,board:chess.board,depth:int,alpha:int,beta:int)->float:
        evaluator= self.evaluator
        if depth == 0:
            return evaluator.evaluate_board(board)
        elif board.turn == chess.WHITE:
            best_score = float("-inf")
            for move in board.legal_moves:
                board.push(move)
                score = self.min_max(board,depth-1,alpha,beta)
                board.pop()
                best_score = max(best_score,score)
                alpha = max(alpha,score)
                if beta <= alpha:
                    break
            return best_score
        elif board.turn == chess.BLACK:
            best_score=float("inf")
            for move in board.legal_moves:
                board.push(move)
                score= self.min_max(board,depth-1,alpha,beta)
                board.pop()
                best_score = min(best_score,score)
                beta = min(beta,score)
                if beta <= alpha:
                    break
            return best_score
