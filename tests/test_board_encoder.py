import chess

from machine_learning.data.encoder import BoardEncoder


def test_starting_position_vector_size():
    board = chess.Board()

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    assert len(vector) == 769


def test_starting_position_piece_count():
    board = chess.Board()

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    piece_features = vector[:768]

    assert sum(piece_features) == 32


def test_starting_position_turn_is_white():
    board = chess.Board()

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    assert vector[768] == 1


def test_piece_counts_per_channel():
    board = chess.Board()

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    expected_counts = [
        8,  # white pawns
        2,  # white knights
        2,  # white bishops
        2,  # white rooks
        1,  # white queen
        1,  # white king
        8,  # black pawns
        2,  # black knights
        2,  # black bishops
        2,  # black rooks
        1,  # black queen
        1,  # black king
    ]

    actual_counts = []

    for channel in range(12):
        start = channel * 64
        end = start + 64

        actual_counts.append(
            sum(vector[start:end])
        )

    assert actual_counts == expected_counts


def test_e2e4_moves_white_pawn():
    board = chess.Board()

    board.push_uci("e2e4")

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    white_pawn_channel = 0

    e2_index = (
        white_pawn_channel * 64
        + chess.E2
    )

    e4_index = (
        white_pawn_channel * 64
        + chess.E4
    )

    assert vector[e2_index] == 0
    assert vector[e4_index] == 1


def test_turn_changes_after_white_move():
    board = chess.Board()

    board.push_uci("e2e4")

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    assert vector[768] == 0


def test_capture_reduces_piece_count():
    board = chess.Board()

    board.push_uci("e2e4")
    board.push_uci("d7d5")
    board.push_uci("e4d5")

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    piece_features = vector[:768]

    assert sum(piece_features) == 31


def test_captured_black_pawn_is_removed():
    board = chess.Board()

    board.push_uci("e2e4")
    board.push_uci("d7d5")
    board.push_uci("e4d5")

    encoder = BoardEncoder(board)
    vector = encoder.encode_board()

    black_pawn_channel = 6

    d5_index = (
        black_pawn_channel * 64
        + chess.D5
    )

    assert vector[d5_index] == 0