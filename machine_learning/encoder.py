import chess


class BoardEncoder():
    PIECE_TO_CHANNEL = {
        (chess.PAWN, chess.WHITE): 0,
        (chess.KNIGHT, chess.WHITE): 1,
        (chess.BISHOP, chess.WHITE): 2,
        (chess.ROOK, chess.WHITE): 3,
        (chess.QUEEN, chess.WHITE): 4,
        (chess.KING, chess.WHITE): 5,

        (chess.PAWN, chess.BLACK): 6,
        (chess.KNIGHT, chess.BLACK): 7,
        (chess.BISHOP, chess.BLACK): 8,
        (chess.ROOK, chess.BLACK): 9,
        (chess.QUEEN, chess.BLACK): 10,
        (chess.KING, chess.BLACK): 11,
    }

    PIECE_FEATURES = 12 * 64
    TURN_FEATURES = 1
    def __init__(self, board: chess.Board):
        self.board = board

    def encode_board(self) -> bytes:
        vector = [0] * (self.PIECE_FEATURES + self.TURN_FEATURES)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                index = self.PIECE_TO_CHANNEL[piece.piece_type,piece.color] * 64 + square
                vector[index] = 1
        turn = 0
        if self.board.turn == chess.WHITE:
            turn =1

        vector[self.PIECE_FEATURES] = turn


        return vector

